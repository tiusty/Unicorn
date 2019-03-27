# Import Django Modules
from django.test import TestCase

# Import Survey Models and forms
from cocoon.survey.models import HomeInformationModel, SurveyUpdateInformation, RentingSurveyModel

# Import Cocoon Modules
from cocoon.houseDatabase.models import RentDatabaseModel
from cocoon.userAuth.models import MyUser


class TestHomeInformationModel(TestCase):

    def test_num_bedrooms_getter(self):
        # Arrange
        survey = HomeInformationModel()

        # i.e they choose only studio
        num_bedrooms_mask = 1
        # Only 1 bedroom
        num_bedrooms_mask1 = 2
        # Only 2 bedrooms
        num_bedrooms_mask2 = 4
        # Only 3 bedrooms
        num_bedrooms_mask3 = 8
        # Only 4 bedrooms
        num_bedrooms_mask4 = 16
        # 1 + 3 bedrooms
        num_bedrooms_mask13 = 10
        # 0 + 2 bedrooms
        num_bedrooms_mask02 = 5
        # 1 + 3 + 4 bedrooms
        num_bedrooms_mask134 = 26
        # 0 + 1 + 2 + 3 + 4 bedrooms
        num_bedrooms_mask01234 = 31

        # Act
        survey.num_bedrooms_bit_masked = num_bedrooms_mask
        self.assertEqual([0], survey.num_bedrooms)
        survey.num_bedrooms_bit_masked = num_bedrooms_mask1
        self.assertEqual([1], survey.num_bedrooms)
        survey.num_bedrooms_bit_masked = num_bedrooms_mask2
        self.assertEqual([2], survey.num_bedrooms)
        survey.num_bedrooms_bit_masked = num_bedrooms_mask3
        self.assertEqual([3], survey.num_bedrooms)
        survey.num_bedrooms_bit_masked = num_bedrooms_mask4
        self.assertEqual([4], survey.num_bedrooms)
        survey.num_bedrooms_bit_masked = num_bedrooms_mask13
        self.assertEqual([1, 3], survey.num_bedrooms)
        survey.num_bedrooms_bit_masked = num_bedrooms_mask02
        self.assertEqual([0, 2], survey.num_bedrooms)
        survey.num_bedrooms_bit_masked = num_bedrooms_mask134
        self.assertEqual([1, 3, 4], survey.num_bedrooms)
        survey.num_bedrooms_bit_masked = num_bedrooms_mask01234
        self.assertEqual([0, 1, 2, 3, 4], survey.num_bedrooms)

    def test_num_bedrooms_setter(self):
        # Arrange
        survey = HomeInformationModel()

        # Act
        survey.num_bedrooms = [0]
        self.assertEqual(1, survey.num_bedrooms_bit_masked)
        survey.num_bedrooms = [1]
        self.assertEqual(2, survey.num_bedrooms_bit_masked)
        survey.num_bedrooms = [2]
        self.assertEqual(4, survey.num_bedrooms_bit_masked)
        survey.num_bedrooms = [3]
        self.assertEqual(8, survey.num_bedrooms_bit_masked)
        survey.num_bedrooms = [4]
        self.assertEqual(16, survey.num_bedrooms_bit_masked)
        survey.num_bedrooms = [1, 3]
        self.assertEqual(10, survey.num_bedrooms_bit_masked)
        survey.num_bedrooms = [2, 4]
        self.assertEqual(20, survey.num_bedrooms_bit_masked)
        survey.num_bedrooms = [0, 1, 2]
        self.assertEqual(7, survey.num_bedrooms_bit_masked)
        survey.num_bedrooms = [0, 2, 4]
        self.assertEqual(21, survey.num_bedrooms_bit_masked)
        survey.num_bedrooms = [0, 1, 2, 3, 4]
        self.assertEqual(31, survey.num_bedrooms_bit_masked)


class TestSurveyUpdateInformation(TestCase):

    def test_blacklisting_homes(self):
        """
        Tests just adding a home to the blacklisted_homes list and making sure it exists in field
        """
        # Arrange
        user = MyUser.objects.create(email="test@test.com")
        survey = RentingSurveyModel.create_survey(user.userProfile)
        home = RentDatabaseModel.create_house_database()

        # Act
        survey.blacklist_home(home)

        # Assert
        self.assertEqual(survey.blacklisted_homes.count(), 1)
        self.assertTrue(survey.blacklisted_homes.filter(id=home.id).exists())

    def test_blacklist_home_homes_already_exist(self):
        """
        Tests adding a home when a home already exists and makes sure both homes are in the list after wards
        """
        # Arrange
        user = MyUser.objects.create(email="test@test.com")
        survey = RentingSurveyModel.create_survey(user.userProfile)
        home = RentDatabaseModel.create_house_database()
        home1 = RentDatabaseModel.create_house_database()
        survey.blacklisted_homes.add(home)

        # Act
        survey.blacklist_home(home1)

        # Assert
        self.assertEqual(survey.blacklisted_homes.count(), 2)
        self.assertTrue(survey.blacklisted_homes.filter(id=home.id).exists())
        self.assertTrue(survey.blacklisted_homes.filter(id=home1.id).exists())

    def tests_adding_same_home_does_not_add_duplicate(self):
        """
        Tests that adding a duplicate home will not cause 2 homes to be in the list
        """
        # Arrange
        user = MyUser.objects.create(email="test@test.com")
        survey = RentingSurveyModel.create_survey(user.userProfile)
        home = RentDatabaseModel.create_house_database()
        survey.blacklisted_homes.add(home)

        # Act
        survey.blacklist_home(home)

        # Assert
        self.assertEqual(survey.blacklisted_homes.count(), 1)
        self.assertTrue(survey.blacklisted_homes.filter(id=home.id).exists())
