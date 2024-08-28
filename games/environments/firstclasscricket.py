import random
import numpy as np

class FirstClassCricket:
    def __init__(self, player_ids):
        ###############################
        # Randomly assign players by ID
        # This aids in game randomization
        ###############################
        assert len(player_ids) == 2, "There must only be two players."
        assert type(player_ids[0]) == str, "Player ID must be of str type."
        assert type(player_ids[1]) == str, "Player ID must be of str type."

        self.player_ids = player_ids

        self.player_one_id = random.choice(player_ids)
        self.player_two_id = player_ids[0] if self.player_one_id == player_ids[1] else player_ids[1]
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

    def step(self, player_inputs):
        assert len(player_inputs) == 2, "There must be two player inputs."
        assert type(player_inputs[0]) == int, "Player input must be of int type."
        assert type(player_inputs[1]) == int, "Player input must be of int type."
        
        if player_inputs[0] == player_inputs[1]:
            # Switching the batting player
            self.batting_player = self.player_two_id if self.batting_player == self.player_one_id else self.player_one_id
            self.fielding_player = self.player_one_id if self.fielding_player == self.player_two_id else self.player_two_id

            if self.round == 2:
                self.round = 1
                self.inning += 1

                # Game end condition
                if self.inning == 4:
                    self.winning_player = self.player_ids(
                        np.argmax([sum(self.player_one_point_history), sum(self.player_two_point_history)])
                    )
                    self.game_over = True
            
            self.round = 2 if self.round == 1 else 1

        elif player_inputs[0] != player_inputs[1]:
            if self.batting_player == self.player_one_id:
                self.player_one_point_history.append(player_inputs[0])
    
            elif self.batting_player == self.player_two_id:
                self.player_two_point_history.append(player_inputs[1])