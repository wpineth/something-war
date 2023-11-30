from agent import *
import random


class RandomAgent(Agent):
    def decide_action(self, game_state):
        options = game_state.get_possible_actions()
        return random.choice(options)
