from googlemaps import distance_matrix, client
from Unicorn.settings.Global_Config import gmaps_api_key
import json

"""
Class that acts as a wrapper for distance matrix requests. Splits requests into 
legal sizes and consolidates results
"""


class DistanceWrapper:

    def __init__(self, key=gmaps_api_key, mode="driving", units="imperial"):
        self.key = key
        self.mode = mode
        self.units = units
        self.client = client.Client(self.key)

    """
    handles any errors thrown by the distance_matrix API
    :param error_code, the error code returned from distance_matrix
    """
    def handle_exception(self, error_code):
        if (error_code == "INVALID_REQUEST"):
            raise Invalid_Request_Exception()
        elif (error_code == "MAX_ELEMENTS_EXCEEDED"):
            raise Max_Elements_Exceeded_Exception()
        elif (error_code == "OVER_QUERY_LIMIT"):
            raise Over_Query_Limit_Exception()
        elif (error_code == "REQUEST_DENIED"):
            raise Request_Denied_Exception()
        elif (error_code == "UNKNOWN_ERROR"):
            raise Unknown_Error_Exception
        elif (error_code == "ZERO_RESULTS"):
            raise Zero_Results_Exception
        else:
            raise Exception("Unidentifiable error in distance_matrix_response")


    """
    Interprets the json response dict from the googlemaps distance_matrix request.
    Handles all errors and combines distances into a list
    :param response_obj, the json response as a dictionary
    :returns a list of lists with tuples (duration, distance) between origins and their destination(s)
    :raises Distance_Matrix_Exception
    """
    def interpret_distance_matrix_response(self, response_obj):
        # check the status
        response_status = response_obj["status"]
        if response_status == "OK":
            distance_list = []

            # each row is an origin
            for row in response_obj["rows"]:
                origin_distance_list = []

                # each element is the origin-destination pairing
                for element in row["elements"]:
                    element_status = element["status"]
                    if element_status == "OK":
                        # retrieve the duration from origin to destination
                        duration_in_seconds = int(element["duration"]["value"])
                        distance_in_meters = int(element["distance"]["value"])
                        origin_distance_list.append((duration_in_seconds, distance_in_meters))
                    # otherwise we skip this origin-destination pairing

                distance_list.append(origin_distance_list)
        else:
            self.handle_exception(response_status)

        # list of lists of durations from origin to destinations
        return distance_list

    """
    Gets the distance matrix corresponding to a destination and an arbitrary number of origins.
    Segments requests to the distance matrix API to include a maximum of 25 origins and returns
    the consolidated results.
    :params origins, list of origins in a distance matrix accepted format
    :params destinations, the destination in a distance matrix accepted format
    :returns a list of lists of tuples containing the duration and distance between the origins and the 
    destination(s).
    :raises DistanceMatrixException on invalid request
    """
    def calculate_distances(self, origins, destinations):

        distance_matrix_list = []

        origin_list = origins
        while origin_list:
            if (len(origin_list) > 25):
                response_json = distance_matrix.distance_matrix(self.client,
                                                                origin_list[:25],
                                                                destinations[:25],
                                                                units=self.units,
                                                                mode=self.mode)
                response_list = self.interpret_distance_matrix_response(response_json)
                for res in response_list:
                    distance_matrix_list.append(res)
                origin_list = origin_list[25:]
            else:
                response_json = distance_matrix.distance_matrix(self.client,
                                                                origin_list,
                                                                destinations[:25],
                                                                units=self.units,
                                                                mode=self.mode)
                # response_dict = json.loads(response_json)

                response_list = self.interpret_distance_matrix_response(response_json)
                for res in response_list:
                    distance_matrix_list.append(res)
                # no origins remaining
                origin_list = []

        # consolidated list containing an inner list for each origin with the duration
        # in minutes to all of its destinations
        return distance_matrix_list

class Distance_Matrix_Exception(Exception):
    pass

class Invalid_Request_Exception(Distance_Matrix_Exception):
    pass

class Max_Elements_Exceeded_Exception(Distance_Matrix_Exception):
    pass

class Over_Query_Limit_Exception(Distance_Matrix_Exception):
    pass

class Request_Denied_Exception(Distance_Matrix_Exception):
    pass

class Unknown_Error_Exception(Distance_Matrix_Exception):
    pass

class Not_Found_Exception(Distance_Matrix_Exception):
    pass

class Zero_Results_Exception(Distance_Matrix_Exception):
    pass

class Max_Route_Length_Exception(Distance_Matrix_Exception):
    pass
