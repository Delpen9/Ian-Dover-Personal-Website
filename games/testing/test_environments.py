import unittest
import numpy as np
import copy

import sys
sys.path.append('../environments')

from firstclasscricket import FirstClassCricket

class TestFirstClassCricket(unittest.TestCase):
    def setUp(self):
        # Set up initial conditions for each test
        self.player_ids = ["player_id_X345", "player_id_Y678"]
        self.cricket_game = FirstClassCricket(self.player_ids)

    def test_initialization(self):
        # Test that the class initializes correctly
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
        
        self.cricket_game.step({"player_id_X345": 1, "player_id_Y678": 1})
        
        self.assertEqual(self.cricket_game.batting_player, previous_fielding_player)
        self.assertEqual(self.cricket_game.fielding_player, previous_batting_player)

    def test_step_add_points(self):
        # Test the step function where points are added for player_one
        self.cricket_game.batting_player = self.cricket_game.player_one_id
        self.cricket_game.fielding_player = self.cricket_game.player_two_id

        self.cricket_game.step({"player_id_X345": 2, "player_id_Y678": 1})
        self.cricket_game.step({"player_id_X345": 1, "player_id_Y678": 1}) # Conclude inning
        self.cricket_game.step({"player_id_X345": 0, "player_id_Y678": 1})

        if self.cricket_game.player_one_id == "player_id_X345":
            self.assertEqual(self.cricket_game.player_one_point_history, [2])

        if self.cricket_game.player_one_id == "player_id_Y678":
            self.assertEqual(self.cricket_game.player_one_point_history, [1])
        
        # Continue to test another round where player_two scores
        self.cricket_game.batting_player = self.cricket_game.player_two_id
        self.cricket_game.fielding_player = self.cricket_game.player_one_id

        self.cricket_game.step({"player_id_X345": 0, "player_id_Y678": 3})
        self.cricket_game.step({"player_id_X345": 1, "player_id_Y678": 1}) # Conclude inning

        if self.cricket_game.player_two_id == "player_id_X345":
            self.assertEqual(self.cricket_game.player_two_point_history, [0])

        if self.cricket_game.player_two_id == "player_id_Y678":
            self.assertEqual(self.cricket_game.player_two_point_history, [3])

    def test_game_end_player_one_win_condition(self):
        # Test that the game ends correctly
        self.cricket_game.inning = 4
        self.cricket_game.round = 2
        self.cricket_game.player_one_point_history = [10, 15]
        self.cricket_game.player_two_point_history = [5, 8]

        self.cricket_game.step({"player_id_X345": 1, "player_id_Y678": 1})
        
        self.assertTrue(self.cricket_game.game_over)
        self.assertEqual(self.cricket_game.winning_player, self.cricket_game.player_one_id)

    def test_game_end_player_two_win_condition(self):
        # Test that the game ends correctly
        self.cricket_game.inning = 4
        self.cricket_game.round = 2
        self.cricket_game.player_one_point_history = [5, 8]
        self.cricket_game.player_two_point_history = [10, 15]

        self.cricket_game.step({"player_id_X345": 1, "player_id_Y678": 1})
        
        self.assertTrue(self.cricket_game.game_over)
        self.assertEqual(self.cricket_game.winning_player, self.cricket_game.player_two_id)

    def test_game_end_in_tie_condition(self):
        self.cricket_game.inning = 4
        self.cricket_game.round = 2

        self.cricket_game.player_one_point_history = [1, 1]
        self.cricket_game.player_two_point_history = [1, 1]

        self.cricket_game.step({"player_id_X345": 1, "player_id_Y678": 1})
        
        self.assertTrue(self.cricket_game.game_over)
        self.assertEqual(self.cricket_game.winning_player, "tie")

    def test_underdog(self):
        self.cricket_game.inning = 3
        self.cricket_game.round = 2
        self.cricket_game.player_one_point_history = [9, 12]
        self.cricket_game.player_two_point_history = [10, 16, 32]

        # Overwrite randomization logic
        self.cricket_game.player_one_id = "player_id_X345"
        self.cricket_game.player_two_id = "player_id_Y678"

        self.cricket_game.batting_player = self.cricket_game.player_one_id
        self.cricket_game.fielding_player = self.cricket_game.player_two_id

        self.cricket_game.step({"player_id_X345": 5, "player_id_Y678": 6})
        self.cricket_game.step({"player_id_X345": 2, "player_id_Y678": 6})
        self.cricket_game.step({"player_id_X345": 6, "player_id_Y678": 6})
        
        self.assertEqual(self.cricket_game.player_one_point_history, [9, 12, 32])

    def test_assertions(self):
        # Test that assertions raise errors when conditions are not met
        with self.assertRaises(AssertionError):
            self.cricket_game.step({"player_id_X345": 1}) # Not enough inputs
        with self.assertRaises(AssertionError):
            self.cricket_game.step({"player_id_X345": "1", "player_id_Y678": 1})  # Non-integer input
        with self.assertRaises(AssertionError):
            self.cricket_game.step({"player_id_X345": 7, "player_id_Y678": 1})  # Input too big
        with self.assertRaises(AssertionError):
            self.cricket_game.step({"player_id_X345": 1, "player_id_Y678": 7})  # Input too big
        with self.assertRaises(AssertionError):
            self.cricket_game.step([1, 5])  # Input of wrong type


if __name__ == '__main__':
    unittest.main()