import random
import numpy as np


class FirstClassCricket:
    def __init__(self, player_ids: list[str, str]):
        ###############################
        # Randomly assign players by ID
        # This aids in game randomization
        ###############################
        assert len(player_ids) == 2, "There must only be two players."
        assert type(player_ids[0]) == str, "Player ID must be of str type."
        assert type(player_ids[1]) == str, "Player ID must be of str type."

        self.player_one_id = random.choice(player_ids)
        self.player_two_id = (
            player_ids[0] if self.player_one_id == player_ids[1] else player_ids[1]
        )
        ###############################

        self.inning = 1
        self.round = 1

        self.player_one_score = 0
        self.player_two_score = 0

        self.player_one_point_history = []
        self.player_two_point_history = []

        self.batting_player = self.player_one_id
        self.fielding_player = self.player_two_id

        self.winning_player = None
        self.game_over = False

    def underdog(self):
        history_length_condition = (
            len(self.player_one_point_history) >= 2
            and len(self.player_two_point_history) >= 2
            and len(self.player_one_point_history) == len(self.player_two_point_history)
        )

        if history_length_condition:
            underdog_condition_for_player_one = (
                self.player_two_point_history[-2]
                < self.player_one_point_history[-2]
            ) and (
                self.player_two_point_history[-1]
                < self.player_one_point_history[-1]
            )

            if underdog_condition_for_player_one:
                self.player_two_point_history[-1] = max(
                    self.player_two_point_history[-1],
                    2 * self.player_one_point_history[-2],
                )

            underdog_condition_for_player_two = (
                self.player_two_point_history[-2]
                > self.player_one_point_history[-2]
            ) and (
                self.player_two_point_history[-1]
                > self.player_one_point_history[-1]
            )

            if underdog_condition_for_player_two:
                self.player_one_point_history[-1] = max(
                    self.player_one_point_history[-1],
                    2 * self.player_two_point_history[-2],
                )

    def step(self, player_inputs: dict):
        assert isinstance(player_inputs, dict), "player_inputs must be of type dict."
        assert len(player_inputs) == 2, "There must be two player inputs."

        # Convert the values to a list first
        player_values = list(player_inputs.values())

        assert isinstance(player_values[0], int), "Player input must be of int type."
        assert isinstance(player_values[1], int), "Player input must be of int type."

        assert player_values[0] < 7, "Player input must be <= 6."
        assert player_values[1] < 7, "Player input must be <= 6."

        if player_values[0] == player_values[1]:
            if self.batting_player == self.player_one_id:
                self.player_one_point_history.append(self.player_one_score)
                self.player_one_score = 0

            elif self.batting_player == self.player_two_id:
                self.player_two_point_history.append(self.player_two_score)
                self.player_two_score = 0

            self.underdog() # runs the underdog condition if applicable

            # Switching the batting player
            self.batting_player = (
                self.player_two_id
                if self.batting_player == self.player_one_id
                else self.player_one_id
            )
            self.fielding_player = (
                self.player_one_id
                if self.fielding_player == self.player_two_id
                else self.player_two_id
            )

            if self.round == 2:
                # Game end condition
                if self.inning == 4:
                    player_one_score = sum(self.player_one_point_history)
                    player_two_score = sum(self.player_two_point_history)

                    if player_one_score > player_two_score:
                        self.winning_player = self.player_one_id
                    elif player_two_score > player_one_score:
                        self.winning_player = self.player_two_id
                    else:
                        self.winning_player = "tie"

                    self.game_over = True

                self.round = 1
                self.inning += 1

            self.round = 2 if self.round == 1 else 1

        elif player_values[0] != player_values[1]:
            if self.batting_player == self.player_one_id:
                self.player_one_score += player_inputs[self.player_one_id]

            elif self.batting_player == self.player_two_id:
                self.player_two_score += player_inputs[self.player_two_id]