# Django modules
from django.test import TestCase
from django.utils import timezone

# Cocoon modules
from cocoon.houseDatabase.models import RentDatabaseModel, HomeTypeModel, HomeProviderModel
import cocoon.houseDatabase.maps_requester as geolocator

# Import script to pull MLSPIN data
from cocoon.houseDatabase.management.commands.pull_mlspin import MlspinRequester

# Import 3rd party modules
from unittest.mock import MagicMock
import os


class TestPullMlspin(TestCase):

    """"
    reads in a file with test data and passes it to the Mls requester
    """
    def setUp(self):

        # Create the manager
        HomeProviderModel.objects.create(provider=HomeProviderModel.MLSPIN)

        # Set up the apartment home type
        self.home_type = HomeTypeModel.objects.create(home_type=HomeTypeModel.APARTMENT)
        with open(os.path.join(os.path.dirname(__file__), "test_idx_feed.txt"), "r") as fp:
            self.idx_data = fp.readlines()
        # self.idx_data = (idx_file.read().decode("iso-8859-1"))

        towns_file = open(os.path.join(os.path.dirname(__file__), "test_towns.txt"), "rb")
        self.towns_data = (towns_file.read().decode("iso-8859-1"))

    def test_idx_parser(self):
        # Arrange
        self.mls_handler = MlspinRequester(timestamp=timezone.now(), pull_idx_feed=False, town_txt=self.towns_data)
        self.mls_handler.idx_txt = self.idx_data

        # Add mock libraries
        geolocator.maps_requester.get_lat_lon_from_address = MagicMock(return_value=(42.408053, -71.163244))

        # Act
        self.mls_handler.parse_idx_feed()

        # assert that the homes exist in the database
        self.assertEqual(RentDatabaseModel.objects.count(), 3)

        # Retrieve homes
        home1 = RentDatabaseModel.objects.get(street_address="12 Mount Vernon St")  # 12 Mount Vernon St.
        home2 = RentDatabaseModel.objects.get(street_address="296 Marlborough St")  # 296 Marlborough St.
        home3 = RentDatabaseModel.objects.get(street_address="784 Tremont Street")  # 784 Tremont St.

        # asserts for the first home
        self.assertEqual(home1.street_address, "12 Mount Vernon St")
        self.assertEqual(home1.city, "Boston")
        self.assertEqual(home1.zip_code, "02129")
        self.assertEqual(home1.price, 3800)
        self.assertEqual(home1.home_type, self.home_type)
        self.assertEqual(str(home1.latitude), "42.408053")
        self.assertEqual(str(home1.longitude), "-71.163244")
        self.assertEqual(home1.state, "MA")
        self.assertEqual(home1.num_bedrooms, 2)
        self.assertEqual(home1.num_bathrooms, 1)
        self.assertEqual(home1.listing_number, 71811023)
        self.assertEqual(home1.listing_agent, "BB808729")
        self.assertEqual(home1.listing_provider, HomeProviderModel.objects.get(provider="MLSPIN"))
        self.assertEqual(home1.listing_office, "AN1037")
        self.assertTrue(home1.parking_spot)

        # asserts for the second home
        self.assertEqual(home2.street_address, "296 Marlborough St")
        self.assertEqual(home2.city, "Boston")
        self.assertEqual(home2.zip_code, "02114")
        self.assertEqual(home2.price, 2850)
        self.assertEqual(home2.home_type, self.home_type)
        self.assertEqual(str(home2.latitude), "42.408053")
        self.assertEqual(str(home2.longitude), "-71.163244")
        self.assertEqual(home2.state, "MA")
        self.assertEqual(home2.num_bedrooms, 1)
        self.assertEqual(home2.num_bathrooms, 1)
        self.assertEqual(home2.listing_number, 71738853)
        self.assertEqual(home2.listing_agent, "BB808729")
        self.assertEqual(home2.listing_provider, HomeProviderModel.objects.get(provider="MLSPIN"))
        self.assertEqual(home2.listing_office, "AN1037")
        self.assertFalse(home2.parking_spot)

        # asserts for the third home
        self.assertEqual(home3.street_address, "784 Tremont Street")
        self.assertEqual(home3.city, "Boston")
        self.assertEqual(home3.zip_code, "02118")
        self.assertEqual(home3.price, 3460)
        self.assertEqual(home3.home_type, self.home_type)
        self.assertEqual(str(home3.latitude), "42.408053")
        self.assertEqual(str(home3.longitude), "-71.163244")
        self.assertEqual(home3.state, "MA")
        self.assertEqual(home3.num_bedrooms, 1)
        self.assertEqual(home3.num_bathrooms, 1)
        self.assertEqual(home3.listing_number, 72080819)
        self.assertEqual(home3.listing_agent, "BB808729")
        self.assertEqual(home3.listing_provider, HomeProviderModel.objects.get(provider="MLSPIN"))
        self.assertEqual(home3.listing_office, "AN1037")
        self.assertTrue(home3.parking_spot)
