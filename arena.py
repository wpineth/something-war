import game
import random_agent
import typing_human_agent
from game import *
from random_agent import *
from typing_human_agent import *


def main():
    game_state = game.Game()
    white_agent = typing_human_agent.TypingHumanAgent()
    black_agent = random_agent.RandomAgent()

    while not game_state.is_terminal():
        if game_state.get_player_to_move() == 1:
            action = white_agent.decide_action(game_state)
        else:
            action = black_agent.decide_action(game_state)

        try:
            game_state.take_action(action)
        except Exception as e:
            print("oops, threw an exception!")
            print(e.args[0])
            print(action.action_type)
            print(action.space)
            print(action.heading)
            print(action.piece_type)
            input("press enter to continue")

    if game_state.get_reward() > 0:
        print("White Wins!")
    if game_state.get_reward() < 0:
        print("Black Wins!")


if __name__ == "__main__":
    main()