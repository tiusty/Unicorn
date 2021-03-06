from django.test import TestCase
from cocoon.scheduler.clientScheduler.client_scheduler import ClientScheduler
from unittest.mock import patch
from cocoon.commutes.constants import CommuteAccuracy

class TestClientScheduler(TestCase):

    def interpret_algorithm_output(self, homes_list, shortest_path):

        """
        Utility function to interpret the shortest path using the home list to make it ready for output onto the main site
        args:
        :param (list) homes_list: The matrix calcualted using DistanceWrapper() with distances between every pair of homes in favorited list
        :param (list) shortest_path: List of indices that denote the shortest path, which is the output of the algorithm
        :return: (list): interpreted_route List of strings containing the addresses in order of the shortest possible path, human readable
        """

        interepreted_route = []

        for item in shortest_path:

            interepreted_route.append((homes_list[item[0]], item[1]))

        return interepreted_route

    def setUp(self):
        self.clientScheduler = ClientScheduler(accuracy=CommuteAccuracy.EXACT)

    @patch('cocoon.scheduler.clientScheduler.client_scheduler.retrieve_exact_commute_client_scheduler')
    def test_build_home_matrix_empty(self, mock_commute):
        '''
        Test to see if empty, should return empty
        :param mock_commute:
        :return:
        '''
        homes_list = []
        mock_commute.return_value = [[]]
        homes_matrix = self.clientScheduler.build_homes_matrix(homes_list)
        self.assertTrue(len(homes_matrix) == 0)

    @patch('cocoon.scheduler.clientScheduler.client_scheduler.retrieve_exact_commute_client_scheduler')
    def test_build_home_matrix_zeros(self, mock_commute):
        '''
        Test to see if all the distances are 0
        :param mock_commute:
        :return:
        '''
        homes_list = ["home1", "home2", "home3"]
        mock_commute.return_value = [[(0,0)],[(0,0)], [(0,2)]]
        homes_matrix = self.clientScheduler.build_homes_matrix(homes_list)
        self.assertEqual(homes_matrix, [[0, 0, 0], [0, 0, 0], [0, 0, 0]])

    @patch('cocoon.scheduler.clientScheduler.client_scheduler.retrieve_exact_commute_client_scheduler')
    def test_build_home_matrix_different_vals(self, mock_commute):
        '''
        Test Case: homes 0,1,2
        0->1 : 1
        0->2 : 2
        1->2 : 3

        :param mock_commute:
        :return:
        '''

        homes_list = ["home1", "home2", "home3"]
        mock_commute.side_effect = [[(0, 0)], [(1, 0)], [(2, 0)]], [[(1, 1)], [(0, 1)], [(3, 1)]], [[(2, 2)], [(3, 2)], [(0, 2)]]
        homes_matrix = self.clientScheduler.build_homes_matrix(homes_list)
        self.assertEqual(homes_matrix, [[0, 1, 2], [1, 0, 3], [2, 3, 0]])

    @patch('cocoon.scheduler.clientScheduler.client_scheduler.retrieve_exact_commute_client_scheduler')
    def test_build_home_matrix_same_distances(self, mock_commute):
        '''
        Test Case: homes 0,1,2
        0->1 : 5
        0->2 : 5
        1->2 : 5

        :param mock_commute:
        :return:
        '''

        homes_list = ["home1", "home2", "home3"]
        mock_commute.side_effect = [[(0, 0)], [(5, 0)], [(5, 0)]], [[(5, 1)], [(0, 1)], [(5, 1)]], [[(5, 2)], [(5, 2)], [(0, 2)]]
        homes_matrix = self.clientScheduler.build_homes_matrix(homes_list)
        self.assertEqual(homes_matrix, [[0, 5, 5], [5, 0, 5], [5, 5, 0]])

    @patch('cocoon.scheduler.clientScheduler.client_scheduler.retrieve_exact_commute_client_scheduler')
    def test_build_home_matrix_decreasing_distances(self, mock_commute):
        '''
        Test Case: homes 0,1,2
        0->1 : 10
        0->2 : 8
        1->2 : 4

        :param mock_commute:
        :return:
        '''

        homes_list = ["home1", "home2", "home3"]

        mock_commute.side_effect = [[(0, 0)], [(10, 0)], [(8, 0)]], [[(10, 0)], [(0, 1)], [(4, 1)]], [[(8, 2)], [(4, 2)], [(0, 2)]]
        homes_matrix = self.clientScheduler.build_homes_matrix(homes_list)
        self.assertEqual(homes_matrix, [[0, 10, 8], [10, 0, 4], [8, 4, 0]])

    @patch('cocoon.scheduler.clientScheduler.client_scheduler.ClientScheduler.build_homes_matrix')
    @patch('cocoon.scheduler.clientScheduler.client_scheduler.clientSchedulerAlgorithm.calculate_path')
    @patch('cocoon.scheduler.clientScheduler.client_scheduler.clientSchedulerAlgorithm.get_edge_weights')
    def test_run_client_scheduler_algorithm(self, mock_edge_weights, mock_shortest_path, mock_build_matrix):
        '''
        Takes in shortest path 1->2->3
        Edge weights 0->5->3
        Should be (1,0) -> (2,5) -> (0,3)
        :param mock_edge_weights:
        :param mock_shortest_path:
        :param mock_build_matrix:
        :return:
        '''

        homes_list = ["home1", "home2", "home3"]

        mock_build_matrix.return_value = [[0, 5, 5], [5, 0, 5], [5, 5, 0]]
        mock_shortest_path.return_value = [1,2,0]
        mock_edge_weights.return_value = [0,5,3]

        tuple_list = self.clientScheduler.run_client_scheduler_algorithm(homes_list)
        self.assertEqual(tuple_list, [("home2",0),("home3",5),("home1",3)])

    def test_interpret_algorithm_output_increasing(self):
        '''
        Straight forward interpretation, should be same as input
        :return:
        '''

        homes_list = ["home1", "home2", "home3"]
        shortest_path = [(0,0), (1,2), (2,3)]
        interpreted_route = self.interpret_algorithm_output(homes_list, shortest_path)
        self.assertEqual(interpreted_route, [("home1",0), ("home2",2), ("home3",3)])

    def test_interpret_algorithm_output_decreasing(self):
        '''
        Straight forward interpretation, should be same as input
        :return:
        '''

        homes_list = ["home1", "home2", "home3"]
        shortest_path = [(2,0), (1,2), (0,1)]
        interpreted_route = self.interpret_algorithm_output(homes_list, shortest_path)
        self.assertEqual(interpreted_route, [("home3",0), ("home2",2), ("home1",1)])

    def test_interpret_algorithm_output_random(self):
        '''
        Straight forward interpretation, should be same as input
        :return:
        '''

        homes_list = ["home1", "home2", "home3"]
        shortest_path = [(1,0),(0,1),(2,3)]
        interpreted_route = self.interpret_algorithm_output(homes_list, shortest_path)
        self.assertEqual(interpreted_route, [("home2",0), ("home1",1), ("home3",3)])