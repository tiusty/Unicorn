from django.test import TestCase
from unittest.mock import MagicMock, patch
from ..distance_wrapper import Request_Denied_Exception, Invalid_Request_Exception, \
    Over_Query_Limit_Exception, Max_Elements_Exceeded_Exception, Unknown_Error_Exception, Zero_Results_Exception, \
    distance_matrix, DistanceWrapper
from ...constants import GoogleCommuteNaming, TRAFFIC_MODEL_BEST_GUESS, TRAFFIC_MODEL_PESSIMISTIC
from ..home_commute import HomeCommute


class TestDistanceWrapper(TestCase):

    def setUp(self):
        self.wrapper = DistanceWrapper()

    def test_request_denied_exception(self):
        response_obj = {
            "destination_addresses": [],
            "error_message": "The provided API key is invalid.",
            "origin_addresses": [],
            "rows": [],
            "status": "REQUEST_DENIED"
        }

        self.assertRaises(Request_Denied_Exception,
                          self.wrapper.interpret_distance_matrix_response, response_obj, 'test', False)

    def test_invalid_request_exception(self):
        response_obj = {
            "destination_addresses": [],
            "error_message": "The provided API key is invalid.",
            "origin_addresses": [],
            "rows": [],
            "status": "INVALID_REQUEST"
        }

        self.assertRaises(Invalid_Request_Exception,
                          self.wrapper.interpret_distance_matrix_response, response_obj, 'test', False)

    def test_over_query_limit_exception(self):
        response_obj = {
            "destination_addresses": [],
            "error_message": "The provided API key is invalid.",
            "origin_addresses": [],
            "rows": [],
            "status": "OVER_QUERY_LIMIT"
        }

        self.assertRaises(Over_Query_Limit_Exception,
                          self.wrapper.interpret_distance_matrix_response, response_obj, 'test', False)

    def test_zero_results_exception(self):
        response_obj = {
            "destination_addresses": [],
            "error_message": "The provided API key is invalid.",
            "origin_addresses": [],
            "rows": [],
            "status": "ZERO_RESULTS"
        }

        self.assertRaises(Zero_Results_Exception,
                          self.wrapper.interpret_distance_matrix_response, response_obj, 'test', False)

    def test_unknown_error_exception(self):
        response_obj = {
            "destination_addresses": [],
            "error_message": "The provided API key is invalid.",
            "origin_addresses": [],
            "rows": [],
            "status": "UNKNOWN_ERROR"
        }

        self.assertRaises(Unknown_Error_Exception,
                          self.wrapper.interpret_distance_matrix_response, response_obj, 'test', False)

    def test_max_elements_exceeded_exception(self):
        response_obj = {
            "destination_addresses": [],
            "error_message": "",
            "origin_addresses": [],
            "rows": [],
            "status": "MAX_ELEMENTS_EXCEEDED"
        }

        self.assertRaises(Max_Elements_Exceeded_Exception,
                          self.wrapper.interpret_distance_matrix_response, response_obj, 'test', False)

    ###############################################
    # API requests required for following functions
    ###############################################

    def test_one_origin_one_destination(self):
        """
        Tests inputting one origin and one destination
        """
        # Arrange
        destination = [
            HomeCommute(address="2 Snow Hill Lane", city="Medfield", state="MA")
        ]
        origin = [
            HomeCommute(address="1 Dewing Path", city="Wellesley", state="MA")
        ]

        # Setting distance matrix output so it doesn't use api calls.
        # If google api response changes, the return value needs to change
        distance_matrix.distance_matrix = MagicMock(return_value={'origin_addresses': ['2 Snow Hill Ln, Medfield, MA 02052, USA'], 'status': 'OK', 'rows': [{'elements': [{'status': 'OK', 'duration': {'text': '15 mins', 'value': 879}, 'distance': {'text': '6.7 mi', 'value': 10747}}]}], 'destination_addresses': ['1 Dewing Path, Wellesley, MA 02482, USA']}
)
        duration_list = self.wrapper.get_durations_and_distances(destination, origin)
        self.assertEqual(len(duration_list), 1)
        self.assertEqual(len(duration_list[0]), 1)
        self.assertEqual(type(duration_list[0][0][0]), int)

    def test_multiple_origins(self):
        """
        Tests inputting two origins and one destination
        """
        # Arrange
        origins = [
            HomeCommute(address="2 Snow Hill Lane", city="Medfield", state="MA"),
            HomeCommute(address='1 Dewing Path', city="Wellesley", state="MA")
        ]
        destinations = [
            HomeCommute(address="350 Prospect Street", city="Belmont", state="MA")
        ]
        # Setting distance matrix output so it doesn't use api calls.
        # If google api response changes, the return value needs to change
        distance_matrix.distance_matrix = MagicMock(return_value={'destination_addresses': ['350 Prospect St, Belmont, MA 02478, USA'], 'status': 'OK', 'rows': [{'elements': [{'status': 'OK', 'duration': {'text': '33 mins', 'value': 1966}, 'distance': {'text': '24.4 mi', 'value': 39311}}]}, {'elements': [{'status': 'OK', 'duration': {'text': '25 mins', 'value': 1479}, 'distance': {'text': '16.3 mi', 'value': 26184}}]}], 'origin_addresses': ['2 Snow Hill Ln, Medfield, MA 02052, USA', '1 Dewing Path, Wellesley, MA 02482, USA']})

        # Act
        duration_list = self.wrapper.get_durations_and_distances(origins, destinations)

        # Assert
        # Given the pre set google api response, make sure the output is correct
        self.assertEqual(len(duration_list), 2)

        # Check the first response
        self.assertEqual(len(duration_list[0]), 1)
        self.assertEqual(type(duration_list[0][0][0]), int)
        self.assertEqual(type(duration_list[0][0][1]), int)
        self.assertEqual(duration_list[0][0][0], 1966)
        self.assertEqual(duration_list[0][0][1], 39311)

        # Check the seconds response
        self.assertEqual(len(duration_list[1]), 1)
        self.assertEqual(type(duration_list[1][0][0]), int)
        self.assertEqual(type(duration_list[1][0][1]), int)
        self.assertEqual(duration_list[1][0][0], 1479)
        self.assertEqual(duration_list[1][0][1], 26184)

    def test_multiple_origins_and_destinations(self):
        """
        Tests inputting 2 origins and 2 destinations.
        """
        # Arrange
        origins = [
            HomeCommute(address="350 Prospect Street", city="Belmont", state="MA"),
            HomeCommute(address="159 Brattle Street", city="Arlington", state="MA")
        ]
        destinations = [
            HomeCommute(address="2 Snow Hill Lane", city="Medfield", state="MA"),
            HomeCommute(address="1 Dewing Path", city="Wellesley", state="MA")
        ]
        distance_matrix.distance_matrix = MagicMock(return_value={'origin_addresses': ['2 Snow Hill Ln, Medfield, MA 02052, USA', '1 Dewing Path, Wellesley, MA 02482, USA'], 'destination_addresses': ['350 Prospect St, Belmont, MA 02478, USA', '159 Brattle St, Arlington, MA 02474, USA'], 'rows': [{'elements': [{'distance': {'text': '24.4 mi', 'value': 39311}, 'duration': {'text': '33 mins', 'value': 1966}, 'status': 'OK'}, {'distance': {'text': '26.0 mi', 'value': 41838}, 'duration': {'text': '39 mins', 'value': 2336}, 'status': 'OK'}]}, {'elements': [{'distance': {'text': '16.3 mi', 'value': 26184}, 'duration': {'text': '25 mins', 'value': 1479}, 'status': 'OK'}, {'distance': {'text': '17.8 mi', 'value': 28711}, 'duration': {'text': '31 mins', 'value': 1849}, 'status': 'OK'}]}], 'status': 'OK'})

        # Act
        duration_list = self.wrapper.get_durations_and_distances(origins, destinations)

        # Assert
        # Given the pre set google api response, make sure the output is correct

        # Assert 2 origins
        self.assertEqual(len(duration_list), 2)

        # Assert 2 destinations with the first origin
        self.assertEqual(len(duration_list[0]), 2)

        # Check the first origin with first destination
        self.assertEqual(duration_list[0][0][0], 1966)
        self.assertEqual(duration_list[0][0][1], 39311)

        # Check the first origin with the second destination
        self.assertEqual(duration_list[0][1][0], 2336)
        self.assertEqual(duration_list[0][1][1], 41838)

        # Assert two destinations with the second origin
        self.assertEqual(len(duration_list[1]), 2)

        # Check the second origin with the first destination
        self.assertEqual(duration_list[1][0][0], 1479)
        self.assertEqual(duration_list[1][0][1], 26184)

        # Check the second origin with the second destination
        self.assertEqual(duration_list[1][1][0], 1849)
        self.assertEqual(duration_list[1][1][1], 28711)

    def test_exceeding_max_num_origins(self):
        """
        Tests to make sure that if 50 origins are given, it can properly split up the response to not hit the
            google api max amount of elements
        """
        # Arrange
        origins = []
        for i in range(50):
            origins.append(HomeCommute(address="2 Snow Hill Lane", city='Medfield', state='MA'))
        destinations = [
            HomeCommute(address='350 Prospect Street', city='Belmont', state='MA'),
            HomeCommute(address='159 Brattle Street', city='Arlington', state='MA')
        ]
        distance_matrix.distance_matrix = MagicMock(return_value={'status': 'OK', 'origin_addresses': ['2 Snow Hill Ln, Medfield, MA 02052, USA', '2 Snow Hill Ln, Medfield, MA 02052, USA', '2 Snow Hill Ln, Medfield, MA 02052, USA', '2 Snow Hill Ln, Medfield, MA 02052, USA', '2 Snow Hill Ln, Medfield, MA 02052, USA', '2 Snow Hill Ln, Medfield, MA 02052, USA', '2 Snow Hill Ln, Medfield, MA 02052, USA', '2 Snow Hill Ln, Medfield, MA 02052, USA', '2 Snow Hill Ln, Medfield, MA 02052, USA', '2 Snow Hill Ln, Medfield, MA 02052, USA', '2 Snow Hill Ln, Medfield, MA 02052, USA', '2 Snow Hill Ln, Medfield, MA 02052, USA', '2 Snow Hill Ln, Medfield, MA 02052, USA', '2 Snow Hill Ln, Medfield, MA 02052, USA', '2 Snow Hill Ln, Medfield, MA 02052, USA', '2 Snow Hill Ln, Medfield, MA 02052, USA', '2 Snow Hill Ln, Medfield, MA 02052, USA', '2 Snow Hill Ln, Medfield, MA 02052, USA', '2 Snow Hill Ln, Medfield, MA 02052, USA', '2 Snow Hill Ln, Medfield, MA 02052, USA', '2 Snow Hill Ln, Medfield, MA 02052, USA', '2 Snow Hill Ln, Medfield, MA 02052, USA', '2 Snow Hill Ln, Medfield, MA 02052, USA', '2 Snow Hill Ln, Medfield, MA 02052, USA', '2 Snow Hill Ln, Medfield, MA 02052, USA'], 'rows': [{'elements': [{'duration': {'value': 1966, 'text': '33 mins'}, 'status': 'OK', 'distance': {'value': 39311, 'text': '24.4 mi'}}, {'duration': {'value': 2336, 'text': '39 mins'}, 'status': 'OK', 'distance': {'value': 41838, 'text': '26.0 mi'}}]}, {'elements': [{'duration': {'value': 1966, 'text': '33 mins'}, 'status': 'OK', 'distance': {'value': 39311, 'text': '24.4 mi'}}, {'duration': {'value': 2336, 'text': '39 mins'}, 'status': 'OK', 'distance': {'value': 41838, 'text': '26.0 mi'}}]}, {'elements': [{'duration': {'value': 1966, 'text': '33 mins'}, 'status': 'OK', 'distance': {'value': 39311, 'text': '24.4 mi'}}, {'duration': {'value': 2336, 'text': '39 mins'}, 'status': 'OK', 'distance': {'value': 41838, 'text': '26.0 mi'}}]}, {'elements': [{'duration': {'value': 1966, 'text': '33 mins'}, 'status': 'OK', 'distance': {'value': 39311, 'text': '24.4 mi'}}, {'duration': {'value': 2336, 'text': '39 mins'}, 'status': 'OK', 'distance': {'value': 41838, 'text': '26.0 mi'}}]}, {'elements': [{'duration': {'value': 1966, 'text': '33 mins'}, 'status': 'OK', 'distance': {'value': 39311, 'text': '24.4 mi'}}, {'duration': {'value': 2336, 'text': '39 mins'}, 'status': 'OK', 'distance': {'value': 41838, 'text': '26.0 mi'}}]}, {'elements': [{'duration': {'value': 1966, 'text': '33 mins'}, 'status': 'OK', 'distance': {'value': 39311, 'text': '24.4 mi'}}, {'duration': {'value': 2336, 'text': '39 mins'}, 'status': 'OK', 'distance': {'value': 41838, 'text': '26.0 mi'}}]}, {'elements': [{'duration': {'value': 1966, 'text': '33 mins'}, 'status': 'OK', 'distance': {'value': 39311, 'text': '24.4 mi'}}, {'duration': {'value': 2336, 'text': '39 mins'}, 'status': 'OK', 'distance': {'value': 41838, 'text': '26.0 mi'}}]}, {'elements': [{'duration': {'value': 1966, 'text': '33 mins'}, 'status': 'OK', 'distance': {'value': 39311, 'text': '24.4 mi'}}, {'duration': {'value': 2336, 'text': '39 mins'}, 'status': 'OK', 'distance': {'value': 41838, 'text': '26.0 mi'}}]}, {'elements': [{'duration': {'value': 1966, 'text': '33 mins'}, 'status': 'OK', 'distance': {'value': 39311, 'text': '24.4 mi'}}, {'duration': {'value': 2336, 'text': '39 mins'}, 'status': 'OK', 'distance': {'value': 41838, 'text': '26.0 mi'}}]}, {'elements': [{'duration': {'value': 1966, 'text': '33 mins'}, 'status': 'OK', 'distance': {'value': 39311, 'text': '24.4 mi'}}, {'duration': {'value': 2336, 'text': '39 mins'}, 'status': 'OK', 'distance': {'value': 41838, 'text': '26.0 mi'}}]}, {'elements': [{'duration': {'value': 1966, 'text': '33 mins'}, 'status': 'OK', 'distance': {'value': 39311, 'text': '24.4 mi'}}, {'duration': {'value': 2336, 'text': '39 mins'}, 'status': 'OK', 'distance': {'value': 41838, 'text': '26.0 mi'}}]}, {'elements': [{'duration': {'value': 1966, 'text': '33 mins'}, 'status': 'OK', 'distance': {'value': 39311, 'text': '24.4 mi'}}, {'duration': {'value': 2336, 'text': '39 mins'}, 'status': 'OK', 'distance': {'value': 41838, 'text': '26.0 mi'}}]}, {'elements': [{'duration': {'value': 1966, 'text': '33 mins'}, 'status': 'OK', 'distance': {'value': 39311, 'text': '24.4 mi'}}, {'duration': {'value': 2336, 'text': '39 mins'}, 'status': 'OK', 'distance': {'value': 41838, 'text': '26.0 mi'}}]}, {'elements': [{'duration': {'value': 1966, 'text': '33 mins'}, 'status': 'OK', 'distance': {'value': 39311, 'text': '24.4 mi'}}, {'duration': {'value': 2336, 'text': '39 mins'}, 'status': 'OK', 'distance': {'value': 41838, 'text': '26.0 mi'}}]}, {'elements': [{'duration': {'value': 1966, 'text': '33 mins'}, 'status': 'OK', 'distance': {'value': 39311, 'text': '24.4 mi'}}, {'duration': {'value': 2336, 'text': '39 mins'}, 'status': 'OK', 'distance': {'value': 41838, 'text': '26.0 mi'}}]}, {'elements': [{'duration': {'value': 1966, 'text': '33 mins'}, 'status': 'OK', 'distance': {'value': 39311, 'text': '24.4 mi'}}, {'duration': {'value': 2336, 'text': '39 mins'}, 'status': 'OK', 'distance': {'value': 41838, 'text': '26.0 mi'}}]}, {'elements': [{'duration': {'value': 1966, 'text': '33 mins'}, 'status': 'OK', 'distance': {'value': 39311, 'text': '24.4 mi'}}, {'duration': {'value': 2336, 'text': '39 mins'}, 'status': 'OK', 'distance': {'value': 41838, 'text': '26.0 mi'}}]}, {'elements': [{'duration': {'value': 1966, 'text': '33 mins'}, 'status': 'OK', 'distance': {'value': 39311, 'text': '24.4 mi'}}, {'duration': {'value': 2336, 'text': '39 mins'}, 'status': 'OK', 'distance': {'value': 41838, 'text': '26.0 mi'}}]}, {'elements': [{'duration': {'value': 1966, 'text': '33 mins'}, 'status': 'OK', 'distance': {'value': 39311, 'text': '24.4 mi'}}, {'duration': {'value': 2336, 'text': '39 mins'}, 'status': 'OK', 'distance': {'value': 41838, 'text': '26.0 mi'}}]}, {'elements': [{'duration': {'value': 1966, 'text': '33 mins'}, 'status': 'OK', 'distance': {'value': 39311, 'text': '24.4 mi'}}, {'duration': {'value': 2336, 'text': '39 mins'}, 'status': 'OK', 'distance': {'value': 41838, 'text': '26.0 mi'}}]}, {'elements': [{'duration': {'value': 1966, 'text': '33 mins'}, 'status': 'OK', 'distance': {'value': 39311, 'text': '24.4 mi'}}, {'duration': {'value': 2336, 'text': '39 mins'}, 'status': 'OK', 'distance': {'value': 41838, 'text': '26.0 mi'}}]}, {'elements': [{'duration': {'value': 1966, 'text': '33 mins'}, 'status': 'OK', 'distance': {'value': 39311, 'text': '24.4 mi'}}, {'duration': {'value': 2336, 'text': '39 mins'}, 'status': 'OK', 'distance': {'value': 41838, 'text': '26.0 mi'}}]}, {'elements': [{'duration': {'value': 1966, 'text': '33 mins'}, 'status': 'OK', 'distance': {'value': 39311, 'text': '24.4 mi'}}, {'duration': {'value': 2336, 'text': '39 mins'}, 'status': 'OK', 'distance': {'value': 41838, 'text': '26.0 mi'}}]}, {'elements': [{'duration': {'value': 1966, 'text': '33 mins'}, 'status': 'OK', 'distance': {'value': 39311, 'text': '24.4 mi'}}, {'duration': {'value': 2336, 'text': '39 mins'}, 'status': 'OK', 'distance': {'value': 41838, 'text': '26.0 mi'}}]}, {'elements': [{'duration': {'value': 1966, 'text': '33 mins'}, 'status': 'OK', 'distance': {'value': 39311, 'text': '24.4 mi'}}, {'duration': {'value': 2336, 'text': '39 mins'}, 'status': 'OK', 'distance': {'value': 41838, 'text': '26.0 mi'}}]}], 'destination_addresses': ['350 Prospect St, Belmont, MA 02478, USA', '159 Brattle St, Arlington, MA 02474, USA']})

        # Act
        duration_list = self.wrapper.get_durations_and_distances(origins, destinations)

        self.assertEqual(len(duration_list), 50)
        for duration in duration_list:
            self.assertEqual(len(duration), 2)
            self.assertEqual(type(duration[0][0]), int)
            self.assertEqual(type(duration[0][1]), int)
            self.assertEqual(type(duration[1][0]), int)
            self.assertEqual(type(duration[1][1]), int)

            self.assertEqual(duration[0][0], 1966)
            self.assertEqual(duration[0][1], 39311)
            self.assertEqual(duration[1][0], 2336)
            self.assertEqual(duration[1][1], 41838)

    @patch('cocoon.commutes.distance_matrix.distance_wrapper.compute_departure_time_without_traffic')
    @patch('cocoon.commutes.distance_matrix.distance_wrapper.compute_departure_time_with_traffic')
    def test_determine_departure_time_driving_traffic(self, mock_with, mock_without):
        """
        Tests that if the commute type is driving and they want traffic then the departure time
            is with traffic
        """
        # Arrange
        mode = GoogleCommuteNaming.DRIVING
        with_traffic = True
        distance_wrapper = DistanceWrapper()

        # Act
        distance_wrapper.determine_departure_time(mode, with_traffic)

        # Assert
        mock_with.assert_called_once_with()
        mock_without.assert_not_called()

    @patch('cocoon.commutes.distance_matrix.distance_wrapper.compute_departure_time_without_traffic')
    @patch('cocoon.commutes.distance_matrix.distance_wrapper.compute_departure_time_with_traffic')
    def test_determine_departure_time_driving_no_traffic(self, mock_with, mock_without):
        """
        Tests that if the commute type is driving and they don't want traffic then the departure time
            is with traffic
        """
        # Arrange
        mode = GoogleCommuteNaming.DRIVING
        with_traffic = False
        distance_wrapper = DistanceWrapper()

        # Act
        distance_wrapper.determine_departure_time(mode, with_traffic)

        # Assert
        mock_with.assert_not_called()
        mock_without.assert_called_once_with()

    @patch('cocoon.commutes.distance_matrix.distance_wrapper.compute_departure_time_without_traffic')
    @patch('cocoon.commutes.distance_matrix.distance_wrapper.compute_departure_time_with_traffic')
    def test_determine_departure_time_driving_transit_with_traffic(self, mock_with, mock_without):
        """
        Tests that if the commute type is transit then the departure time
            is with traffic even if with traffic is specified
        """
        # Arrange
        mode = GoogleCommuteNaming.TRANSIT
        with_traffic = True
        distance_wrapper = DistanceWrapper()

        # Act
        distance_wrapper.determine_departure_time(mode, with_traffic)

        # Assert
        mock_with.assert_called_once_with()
        mock_without.assert_not_called()

    @patch('cocoon.commutes.distance_matrix.distance_wrapper.compute_departure_time_without_traffic')
    @patch('cocoon.commutes.distance_matrix.distance_wrapper.compute_departure_time_with_traffic')
    def test_determine_departure_time_driving_transit_with_no_traffic(self, mock_with, mock_without):
        """
        Tests that if the commute type is transit then the departure time
            is with traffic even if with no traffic is specified
        """
        # Arrange
        mode = GoogleCommuteNaming.TRANSIT
        with_traffic = False
        distance_wrapper = DistanceWrapper()

        # Act
        distance_wrapper.determine_departure_time(mode, with_traffic)

        # Assert
        mock_with.assert_called_once_with()
        mock_without.assert_not_called()

    def test_interpret_distance_matrix_response_driving_traffic(self):
        """
        Tests that if traffic is desired then the traffic duration is taken
        """
        # Arrange
        mode = GoogleCommuteNaming.DRIVING
        with_traffic = True
        response = {'status': 'OK', 'destination_addresses': ['1245 Massachusetts Ave, Arlington, MA 02476, USA'], 'origin_addresses': ['349 Pleasant St, Malden, MA 02148, USA', '10 Wait St, Boston, MA 02120, USA'], 'rows': [{'elements': [{'distance': {'text': '6.0 mi', 'value': 9650}, 'status': 'OK', 'duration_in_traffic': {'text': '25 mins', 'value': 1492}, 'duration': {'text': '22 mins', 'value': 1298}}]}, {'elements': [{'distance': {'text': '10.8 mi', 'value': 17326}, 'status': 'OK', 'duration_in_traffic': {'text': '44 mins', 'value': 2640}, 'duration': {'text': '29 mins', 'value': 1749}}]}]}
        distance_wrapper = DistanceWrapper()

        # Act
        result = distance_wrapper.interpret_distance_matrix_response(response, mode, with_traffic)

        # Assert
        self.assertEqual(result, [[(1492, 9650)], [(2640, 17326)]])

    def test_interpret_distance_matrix_response_driving_no_traffic(self):
        """
        Tests that if traffic is not desired then the non traffic duration is taken
        """
        # Arrange
        mode = GoogleCommuteNaming.DRIVING
        with_traffic = False
        response = {'status': 'OK', 'destination_addresses': ['1245 Massachusetts Ave, Arlington, MA 02476, USA'], 'origin_addresses': ['349 Pleasant St, Malden, MA 02148, USA', '10 Wait St, Boston, MA 02120, USA'], 'rows': [{'elements': [{'distance': {'text': '6.0 mi', 'value': 9650}, 'status': 'OK', 'duration_in_traffic': {'text': '25 mins', 'value': 1492}, 'duration': {'text': '22 mins', 'value': 1298}}]}, {'elements': [{'distance': {'text': '10.8 mi', 'value': 17326}, 'status': 'OK', 'duration_in_traffic': {'text': '44 mins', 'value': 2640}, 'duration': {'text': '29 mins', 'value': 1749}}]}]}
        distance_wrapper = DistanceWrapper()

        # Act
        result = distance_wrapper.interpret_distance_matrix_response(response, mode, with_traffic)

        # Assert
        self.assertEqual(result, [[(1298, 9650)], [(1749, 17326)]])

    def test_determine_traffic_model_driving_with_traffic(self):
        """
        If the use is driving and wants traffic then pessimistic traffic model should be used
        """
        # Arrange
        mode = GoogleCommuteNaming.DRIVING
        with_traffic = True
        distance_wrapper = DistanceWrapper()

        # Act
        result = distance_wrapper.determine_traffic_model(mode, with_traffic)

        # Assert
        self.assertEqual(result, TRAFFIC_MODEL_PESSIMISTIC)

    def test_determine_traffic_model_driving_with_no_traffic(self):
        """
        If the use is driving and doesn't want traffic then best guess traffic model should be used
        """
        # Arrange
        mode = GoogleCommuteNaming.DRIVING
        with_traffic = False
        distance_wrapper = DistanceWrapper()

        # Act
        result = distance_wrapper.determine_traffic_model(mode, with_traffic)

        # Assert
        self.assertEqual(result, TRAFFIC_MODEL_BEST_GUESS)

    def test_determine_traffic_model_transit_no_traffic(self):
        """
        If the use is transit and doesn't want traffic then best guess traffic model should be used
        """
        # Arrange
        mode = GoogleCommuteNaming.TRANSIT
        with_traffic = False
        distance_wrapper = DistanceWrapper()

        # Act
        result = distance_wrapper.determine_traffic_model(mode, with_traffic)

        # Assert
        self.assertEqual(result, TRAFFIC_MODEL_BEST_GUESS)

    def test_determine_traffic_model_transit_traffic(self):
        """
        If the use is transit and wants traffic then best guess traffic model should be used
        """
        # Arrange
        mode = GoogleCommuteNaming.TRANSIT
        with_traffic = True
        distance_wrapper = DistanceWrapper()

        # Act
        result = distance_wrapper.determine_traffic_model(mode, with_traffic)

        # Assert
        self.assertEqual(result, TRAFFIC_MODEL_BEST_GUESS)
