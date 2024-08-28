import unittest
import numpy as np
import copy

import sys
sys.path.append('../environments')

from firstclasscricket import FirstClassCricket

class TestFirstClassCricket(unittest.TestCase):
    def setUp(self):
        # Set up initial conditions for each test
        self.player_ids = ["player1", "player2"]
        self.cricket_game = FirstClassCricket(self.player_ids)

    def test_initialization(self):
        # Test that the class initializes correctly
        self.assertEqual(len(self.cricket_game.player_ids), 2)
        self.assertIn(self.cricket_game.player_one_id, self.player_ids)
        self.assertIn(self.cricket_game.player_two_id, self.player_ids)
        self.assertNotEqual(self.cricket_game.player_one_id, self.cricket_game.player_two_id)
        self.assertEqual(self.cricket_game.inning, 1)
        self.assertEqual(self.cricket_game.round, 1)
        self.assertEqual(self.cricket_game.player_one_score, 0)
        self.assertEqual(self.cricket_game.player_two_score, 0)
        self.assertIsNone(self.cricket_game.winning_player)
        self.assertFalse(self.cricket_game.game_over)

    def test_step_switch_players(self):
        # Test the step function where players switch
        self.cricket_game.inning = 1  # Ensure we do not trigger end game condition
        
        previous_batting_player = copy.deepcopy(self.cricket_game.batting_player)
        previous_fielding_player = copy.deepcopy(self.cricket_game.fielding_player)
        
        self.cricket_game.step([1, 1])
        
        self.assertEqual(self.cricket_game.batting_player, previous_fielding_player)
        self.assertEqual(self.cricket_game.fielding_player, previous_batting_player)

    def test_step_add_points(self):
        # Test the step function where points are added for player_one
        self.cricket_game.batting_player = self.cricket_game.player_one_id
        self.cricket_game.fielding_player = self.cricket_game.player_two_id

        self.cricket_game.step([2, 1])
        self.assertEqual(self.cricket_game.player_one_point_history, [2])
        self.assertEqual(self.cricket_game.player_two_point_history, [])
        
        # Continue to test another round where player_two scores
        self.cricket_game.batting_player = self.cricket_game.player_two_id
        self.cricket_game.fielding_player = self.cricket_game.player_one_id

        self.cricket_game.step([0, 3])
        self.assertEqual(self.cricket_game.player_one_point_history, [2])
        self.assertEqual(self.cricket_game.player_two_point_history, [3])

    def test_game_end_condition(self):
        # Test that the game ends correctly
        self.cricket_game.inning = 4
        self.cricket_game.round = 2
        self.cricket_game.player_one_point_history = [10, 15]
        self.cricket_game.player_two_point_history = [5, 8]

        self.cricket_game.step([1, 1])
        
        self.assertTrue(self.cricket_game.game_over)
        self.assertEqual(self.cricket_game.winning_player, self.player_ids[0])

    def test_assertions(self):
        # Test that assertions raise errors when conditions are not met
        with self.assertRaises(AssertionError):
            self.cricket_game.step([1])  # Not enough inputs
        with self.assertRaises(AssertionError):
            self.cricket_game.step(["1", 1])  # Non-integer input
        with self.assertRaises(AssertionError):
            self.cricket_game.step([7, 1])  # Input too big
        with self.assertRaises(AssertionError):
            self.cricket_game.step([1, 7])  # Input too big


if __name__ == '__main__':
    unittest.main()