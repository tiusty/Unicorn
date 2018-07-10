# noinspection PyPackageRequirements
import urllib.request
import urllib.error
import cocoon.houseDatabase.maps_requester as geolocator
import os, sys
from django.core.management.base import BaseCommand
from cocoon.houseDatabase.models import HousePhotos, RentDatabaseModel
from cocoon.houseDatabase.management.commands.mls_fields import *
from config.settings.Global_Config import gmaps_api_key
from cocoon.houseDatabase.models import HomeTypeModel, MlsManagementModel
from django.utils import timezone
from ftplib import FTP
from django.core.files.images import ImageFile
import tempfile


class MlspinRequester:
    """
    This class contains the logic for parsing the IDX (Internet Data Exchange)
    feed from MLSPIN and adding apartments to the database. It has been abstracted
    out of the Command class so it can be tested easily.
    Attributes:
        self.NUM_COLS (int): the number of columns in the txt file returned by MLSPIN
        self.idx_txt (String): the pipe delimited txt file containing apartment data
        self.town_txt (String): the pipe delimited txt file containing town codes
    """

    NUM_COLS = 29

    def __init__(self, idx_data, town_data):
        """
        Retrieves IDX feed data from MLSPIN, including txt formatted information on
        over 4000 apartments in Massachusetts.
        """

        self.idx_txt = idx_data
        self.town_txt = town_data

        # Builds a dictionary of town codes to towns
        self.towns = {}
        self.town_lines = self.town_txt.split('\n')
        for line in self.town_lines[1:-1]: # skips the col headers
            fields = line.split('|')
            self.towns[str(fields[0])] = {
                "town":fields[1],
                "county":fields[2],
                "state":fields[3]
            }

    def parse_idx_feed(self):

        lines = self.idx_txt.split('\r\n')
        print("Attempting to add *" + str(len(lines)) + "* apartments to the db...")
        print("An equivalent number of requests will be made to the geocoder")

        # Generate values for the different error cases for tracking purposes
        num_apartments_failed_to_update = 0
        num_apartments_failed_geolocate = 0
        num_apartments_not_for_rental = 0
        num_apartments_with_value_error = 0

        # Parses the IDX txt
        update_timestamp = timezone.now()
        for line in lines[1:-1]:  # skips the col headers

            # Parse IDX feed to put each item into an array
            cells = line.split('|')
            # Make sure there are no commas in the street name
            cells[STREET_NAME].replace(',', '')
            split_address = cells[STREET_NAME].split()
            apartment_no = ""
            clean_address = ""

            try:
                # check for presence of apartment number with int()
                int(cells[STREET_NAME][len(cells[STREET_NAME])-1])
                apartment_no = split_address[len(split_address)-1]
                clean_address = " ".join(split_address[:-1])
            # no int in last address element (not an apartment #)
            except ValueError:
                clean_address = " ".join(split_address)

            # Generate each component for the home address
            town = (self.towns[str(cells[TOWN_NUM])]["town"])
            state = (self.towns[str(cells[TOWN_NUM])]["state"])
            address = ((cells[STREET_NO]) + ' ' + clean_address)
            zip_code = cells[ZIP_CODE]

            # Full address for the geolocator
            full_add = address + ' ' + town + ' ' + state + ' ' + zip_code

            if RentDatabaseModel.objects.filter(listing_number_home=cells[LIST_NO]).exists():
                # If the apartment already exists, verify that the address is the same, if it is then continue,
                #   otherwise throw an error (just for testing purposes to see if it happens). If we decide this is a
                #   non-issue, we can take this out
                existing_apartment = RentDatabaseModel.objects.get(listing_number_home=cells[LIST_NO])
                if existing_apartment.street_address == address and existing_apartment.zip_code == zip_code:
                    existing_apartment.last_updated = update_timestamp
                    existing_apartment.currently_available = True
                    existing_apartment.save()
                    print("[ UPDATING ]" + full_add)
                else:
                    print("Attempting to add home with address {0}".format(full_add))
                    print("Home address that was in the database was {0}".format(existing_apartment.street_address))
                    num_apartments_failed_to_update += 1
            else:
                # If the apartment listing_number did not already exist then add an entry in the database

                # Pulls lat/lon based on address
                locator = geolocator.maps_requester(gmaps_api_key)
                latlng = locator.get_lat_lon_from_address(full_add)

                if latlng == -1:
                    print("Could not generate Lat and Long for apartment {0}, which had line {1} in IDX feed".format(
                        full_add, line
                    ))
                    num_apartments_failed_geolocate += 1
                    continue
                else:
                    lat = latlng[0]
                    lng = latlng[1]

                # Now that the latlng were generated, start creating the apartment

                # Create the new home
                new_listing = RentDatabaseModel()
                # Define the home type
                list_type = cells[PROP_TYPE]

                # verifies unit is a rental (RN denotes rental in MLS feed)
                if list_type == "RN":
                    apartment_home_type = HomeTypeModel.objects.get(home_type_survey="Apartment")
                else:
                    # Since we only support rentals right now we don't want to retrieve any other home types
                    print("Home not a rental, continuing. Error was with line {0}".format(line))
                    num_apartments_not_for_rental += 1
                    continue

                # If any of the fields give a value error, then don't save the apartment
                try:
                    # Set the HomeBaseModel Fields
                    new_listing.street_address = address
                    new_listing.city = town
                    new_listing.state = state
                    new_listing.zip_code = zip_code
                    new_listing.price = int(cells[LIST_PRICE])
                    new_listing.latitude = lat
                    new_listing.longitude = lng

                    # Set InteriorAmenitiesModel Fields
                    # Currently don't support non-integers for num_bathrooms. Therefore
                    #   The num of full and half baths are added then rounded to the nearest int
                    num_baths = int(cells[NO_FULL_BATHS]) + int(cells[NO_HALF_BATHS])
                    new_listing.bath = True if num_baths > 0 else False
                    new_listing.num_bathrooms = num_baths
                    new_listing.num_bedrooms = int(cells[NO_BEDROOMS])

                    # Set MLSpinDataModel fields
                    new_listing.remarks = cells[REMARKS]
                    new_listing.listing_number = int(cells[LIST_NO])
                    new_listing.listing_provider = "MLSPIN"
                    new_listing.listing_agent = cells[LIST_AGENT]
                    new_listing.listing_office = cells[LIST_OFFICE]
                    new_listing.last_updated = update_timestamp

                    # Set RentDatabaseModel fields
                    new_listing.apartment_number = apartment_no
                    new_listing.home_type = apartment_home_type
                    new_listing.currently_available = True

                except ValueError:
                    print("Home could not be added. Error is with line: {0}".format(line))
                    num_apartments_with_value_error += 1
                    continue

                # After all the data is added, save the home to the database
                new_listing.save()

                # Need to parse the listing numbers to find the location of the photos.
                # The directory goes like photo/##/###/###_#.jpg
                # The 8 numbers correspond to the mlspin number
                if new_listing.listing_number > 0:
                    first_directory = str(new_listing.listing_number)[:2]
                    second_directory = str(new_listing.listing_number)[2:5]
                    file_name = str(new_listing.listing_number)[5:9]
                    ftp = FTP("ftp.mlspin.com", "anonymous", "")
                    ftp.login()
                    file_names = list(filter(lambda x: file_name in x, ftp.nlst(os.path.join('photo', first_directory, second_directory))))
                    for file in file_names:
                        lf = tempfile.TemporaryFile("wb+")
                        ftp.retrbinary("RETR " + file, lf.write)
                        new_photos = HousePhotos(house=new_listing)
                        myfile = ImageFile(lf)
                        new_photos.save()
                        new_photos.image.save(os.path.basename(file), myfile)
                        new_photos.save()
                        lf.close()
                else:
                    print("Not adding photo for house")
                print("[ ADDING   ]" + full_add)

        # When all the homes are added, update the MLSManagement model to reflex that the homes have been updated
        print("Updating MLS timestamp to {0}".format(update_timestamp.date()))

        # Printing out errors for data collection and observation
        print()
        print("The following errors were observed:")
        print("Number of homes that failed to update due to address mismatch with same MLS_listing_number: {0}".format(
            num_apartments_failed_to_update
        ))
        print("Number of homes that failed due to failing getting lat + lng: {0}",format(
            num_apartments_failed_geolocate
        ))
        print("Number of homes that failed due to not being for rental: {0}".format(
            num_apartments_not_for_rental
        ))
        print("Number of homes that failed due to Value Error: {0}".format(num_apartments_with_value_error))

        manager = MlsManagementModel.objects.all().first()
        manager.last_updated_mls = update_timestamp
        manager.save()


class Command(BaseCommand):
    """
    Command class that creates an MlsPinRequester object and requests the URL
    of the apartments and towns txt files. This command is accessible via manage.py
    """

    help = 'Ingests IDX feed into database'

    def add_arguments(self, parser):
        # add args here
        return

    def handle(self, *args, **options):
        # reads the apartment data into memory and passes it to the mlspin_handler

        URL = ("http://idx.mlspin.com/idx.asp?user=2K7zB9ytn1MtTtUNFsBtm2R7rZtjfWdyY"
               "aLtNzY2zPPhe2PuDtDK1mP2HrZhPFoE5NND4c7vZPNmNRxItmOLAf2DqO0oDPxUyPn&proptype=RN")

        # 1. Connect to mlspin IDX (internet data exchange URL)
        try:
            urllib.request.urlretrieve(URL, os.path.join(os.path.dirname(__file__), "idx_feed.txt"))
        except (urllib.error.HTTPError, urllib.error.URLError):
            print("Error connecting to MLSPIN")
            sys.exit()

        # 2. Read the response txt into memory
        idx_file = open(os.path.join(os.path.dirname(__file__), "idx_feed.txt"), "rb")
        idx_txt = (idx_file.read().decode("iso-8859-1"))

        towns_file = open(os.path.join(os.path.dirname(__file__), "towns.txt"), "rb")
        town_txt = (towns_file.read().decode("iso-8859-1"))

        print("Successfully read in IDX files")

        mls_handler = MlspinRequester(idx_txt, town_txt)
        mls_handler.parse_idx_feed()
