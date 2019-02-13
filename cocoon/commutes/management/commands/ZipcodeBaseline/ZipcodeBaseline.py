import json
import os
from datetime import timedelta
import random
from django.utils import timezone

from ....models import ZipCodeChild, ZipCodeBase

# import googlemaps API
from click._compat import raw_input

# Retrieve Constants
from cocoon.commutes.models import CommuteType
from cocoon.commutes.distance_matrix.commute_retriever import retrieve_exact_commute

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class ZipcodeBaseline(object):
    JSON_DURATION_KEY_NAME = "duration_seconds"
    JSON_DISTANCE_KEY_NAME = "distance_meters"

    def create_baseline(self, commute_type):
        """
        Generates a baseline for the zipcodes stored in the zip_codes_ files. The zipcodes distances
            and durations are computed using google information and then stored into a file

        :param commute_type: (CommuteType model) -> The commute type that the baseline is being made for

        The format of the file follows below for each parent and child zipcode
            {
                'parent zipcode':
                   {
                        'child_zipcode' :
                        {
                            commute data for the child zipcode
                        }
                   }
            }
        """

        # This function should not be run unless indicated.
        #   this prevent a user running the function by accident
        verify = raw_input("Please don't run this script unless you are directed to, type 'confirm-running' to run: ")
        if verify != "confirm-running":
            exit()

        # Read in all the zipcodes to compute
        # Data stored in a set to prevent duplicates
        list_zip_codes = set()
        with open(BASE_DIR + "/zip_codes_MA.txt", "r") as f:
            for line in f:
                line = line.split()
                list_zip_codes.add(str(line[0]))

        # Turn the set into a list
        list_zip_codes = list(list_zip_codes)

        # Retrieve all the zipcode combinations computed from google
        zipcode_combinations = self.generate_zipcode_combinations(list_zip_codes, commute_type)

        # Now write the result to the file
        filename = BASE_DIR + "/baselines/zipcode_baseline_" + commute_type.get_commute_type_display() + ".json"
        with open(filename, "w") as f:
            f.write(json.dumps(zipcode_combinations))

    @staticmethod
    def generate_zipcode_combinations(list_zip_codes, commute_type):
        """
        :param list_zip_codes: list of zip codes in the Boston area
        :param commute_type: (string) -> The commute type of the baseline that is being created
        :return:

        Function calls the Google Maps Distance Matrix API for every possible combination of Boston zip codes.
        The response object is then parsed for distance and duration in m, s respectively. This data is then used
        to create a dictionary, which is ultimately written to approximations.txt as a json object.
        """
        # Create all the combinations
        zipcode_combinations = {}
        for base_zip in list_zip_codes:

                # Retrieve the combination from Google
                results = retrieve_exact_commute(list_zip_codes,
                                                 base_zip,
                                                 mode=commute_type)

                # Store the results in python
                child_zipcodes = {}
                for commute in range(len(results)):
                    child_zipcodes[list_zip_codes[commute]] = {
                        ZipcodeBaseline.JSON_DURATION_KEY_NAME: results[commute][0][0],
                        ZipcodeBaseline.JSON_DISTANCE_KEY_NAME: results[commute][0][1]
                    }
                zipcode_combinations[base_zip] = child_zipcodes
        return zipcode_combinations

    def load_zipcode_combinations(self, commute_type):
        """
        :param
        :param
        :return:

        Looks into ZipCodeBase database and creates all possible combinations and allows sends errors if approximations
        don't match baselines
        """

        stored_zipcode_combinations = self.pull_stored_zipcode_data(commute_type)

        filename = BASE_DIR + "/baselines/zipcode_baseline_" + commute_type.get_commute_type_display() + ".json"
        with open(filename, "r") as f:
            data = json.load(f)
            for base_zipcode in data:
                for child_zipcode in data[base_zipcode]:
                    # Check to see if the combination exists in the database
                    #   if not then create the pair using the data from the file
                    if not self.check_key(stored_zipcode_combinations, base_zipcode, child_zipcode):
                        zip_code_base = ZipCodeBase.objects.get_or_create(zip_code=base_zipcode)[0]
                        zip_code_base.zipcodechild_set.create(
                            zip_code=child_zipcode,
                            commute_distance_meters=data[base_zipcode][child_zipcode][self.JSON_DISTANCE_KEY_NAME],
                            commute_time_seconds=data[base_zipcode][child_zipcode][self.JSON_DURATION_KEY_NAME],
                            commute_type=commute_type,
                        )

    @staticmethod
    def pull_stored_zipcode_data(commute_type):
        """
        Pulls the zipcode data from the database and stores them in a python
            dictionary
        :param commute_type: (CommuteType Model) -> The commute type the user indicated
        :return: (dict(dict()) -> The dictionary of dictionaries of the data stored in the backend

        The format follows below for each parent and child zipcode
            {
                'parent zipcode':
                   {
                        'child_zipcode' :
                        {
                            commute data for the child zipcode
                        }
                   }
            }
        """
        base_zipcodes = {}
        for zipcode_base in ZipCodeBase.objects.all():
            # Retrieve all the child zip_codes for the destination commute_type
            child_zips = zipcode_base.zipcodechild_set.filter(commute_type=commute_type) \
                .values_list('zip_code', 'commute_time_seconds', 'commute_distance_meters')

            # Dictionary Compression to retrieve the values from the QuerySet
            child_zip_codes = {zip_code: {
                 ZipcodeBaseline.JSON_DURATION_KEY_NAME: commute_time_seconds,
                 ZipcodeBaseline.JSON_DISTANCE_KEY_NAME: commute_distance_meters,
            }
                for zip_code, commute_time_seconds, commute_distance_meters
                in child_zips}

            base_zipcodes[zipcode_base.zip_code] = child_zip_codes
        return base_zipcodes

    @staticmethod
    def check_key(data, base_key, child_key):
        """
        Checks if the keys exists within the base dictionary and the child dictionary
        :param data: (Dictionary) -> The data that the key is being checked in
        :param base_key: (string) -> The parent key of the dictionary
        :param child_key: (string) -> The child key of the dictionary
        :return: (Boolean) -> True: The keys exist within the data, note: Both must exist
                              False: -> Either one or both of the keys do not exist within the data
        """

        if base_key in data:
            if child_key in data[base_key]:
                return True
        return False
