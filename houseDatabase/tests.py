# Django modules
from django.test import TestCase
from django.db import IntegrityError

# House Database models
from houseDatabase.models import ZipCodeDictionaryParent

# Import Global Config
from Unicorn.settings.Global_Config import COMMUTE_TYPES


class ZipCodeDictionaryTest(TestCase):

    def setUp(self):
        self.zip_code = "02476"
        self.zip_code1 = "02474"
        self.zip_code2 = "02467"
        self.commute_time = 4500
        self.commute_distance = 700
        self.commute_type = "driving"

    @staticmethod
    def create_zip_code_dictionary(zip_code):
        """
        Creates a parent zip_code_dictionary object
        :param zip_code: String -> Zip code for parent zipcode
        :return: ZipCodeDiciontaryParent -> An object instance
        """
        return ZipCodeDictionaryParent.objects.create(_zip_code=zip_code)

    @staticmethod
    def create_zip_code_dictionary_child(parent_zip_code_dictionary, zip_code, commute_time,
                                         commute_distance, commute_type):
        """
        Creates a child zip code dictionary for the parent zip code object
        :param parent_zip_code_dictionary: ZipCodeDictionaryParent -> An object instance
        :param zip_code: String -> Zipcode for the child dictionary
        :param commute_time: Int -> The commute time for the child dictionary in seconds
        :param commute_distance: Int -> The commute distance for the child dictionary in meters
        :param commute_type: Commute Type Enum -> Enum for the different commute types
        :return:
        """
        parent_zip_code_dictionary.zipcodedictionarychild_set.create(
            _zip_code=zip_code,
            _commute_time_seconds=commute_time,
            _commute_distance_meters=commute_distance,
            _commute_type=commute_type,
        )

    def test_zip_code_dictionary_parent_working(self):
        # Arrange/ Act
        parent_zip_code = self.create_zip_code_dictionary(self.zip_code)

        # Assert
        self.assertEqual(self.zip_code, parent_zip_code.zip_code)

    def test_zip_code_dictionary_parent_all_working_child(self):
        # Arrange/ Act / Assert // not really following methodology
        # Adding zip code 1
        try:
            self.create_zip_code_dictionary(self.zip_code)
        except IntegrityError:
            self.assertTrue(False, "Integrity exception should not have been raised")

        # Adding zip code 1
        try:
            self.create_zip_code_dictionary(self.zip_code1)
        except IntegrityError:
            self.assertTrue(False, "Integrity exception should not have been raised")

        # Adding zip code 1
        try:
            self.create_zip_code_dictionary(self.zip_code2)
        except IntegrityError:
            self.assertTrue(False, "Integrity exception should not have been raised")

        # All the adding should pass and finish successfully
        self.assertTrue(True)

    def test_zip_code_dictionary_parent_error_adding_duplicate_error_child(self):
        # Arrange/ Act / Assert // not really following methodology
        # Adding zip code 1
        try:
            self.create_zip_code_dictionary(self.zip_code)
        except IntegrityError:
            self.assertTrue(False, "Integrity exception should not have been raised")

        # Act
        try:
            self.create_zip_code_dictionary(self.zip_code)
            self.assertTrue(False, "Integrity exception should have been raised")
        except IntegrityError:
            self.assertTrue(True)

    def test_zip_code_dictionary_parent_error_adding_duplicate_third_child(self):
        # Arrange/ Act / Assert // not really following methodology

        # Adding zip code 1
        try:
            self.create_zip_code_dictionary(self.zip_code)
        except IntegrityError:
            self.assertTrue(False, "Integrity exception should not have been raised")

        # Adding zip code 2
        try:
            self.create_zip_code_dictionary(self.zip_code1)
        except IntegrityError:
            self.assertTrue(False, "Integrity exception should not have been raised")

        # Adding zip code 3, should fail
        try:
            self.create_zip_code_dictionary(self.zip_code)
            self.assertTrue(False, "Integrity exception should have been raised")
        except IntegrityError:
            self.assertTrue(True)

    def test_zip_code_dictionary_child_name(self):
        # Arrange
        parent_zip_code = self.create_zip_code_dictionary(self.zip_code)

        # Act
        self.create_zip_code_dictionary_child(parent_zip_code, self.zip_code, self.commute_time,
                                              self.commute_distance, self.commute_type)

        # Assert
        self.assertEqual(parent_zip_code, parent_zip_code.zipcodedictionarychild_set.first().base_zip_code)
        self.assertEqual(self.zip_code, parent_zip_code.zipcodedictionarychild_set.first().zip_code)
        self.assertEqual(self.commute_time, parent_zip_code.zipcodedictionarychild_set.first().commute_time_seconds)
        self.assertEqual(self.commute_time/60, parent_zip_code.zipcodedictionarychild_set.first().commute_time_minutes)
        self.assertEqual(self.commute_distance, parent_zip_code.zipcodedictionarychild_set.first()
                         .commute_distance_meters)
        self.assertEqual(self.commute_distance * 0.000621371, parent_zip_code.zipcodedictionarychild_set.first()
                         .commute_distance_miles)
        self.assertEqual(self.commute_type, parent_zip_code.zipcodedictionarychild_set.first().commute_type)


