import game
import random_agent
import typing_human_agent
import ai_agent


def main():
    game_state = game.Game()
    turn_num = 0

    # white_agent = typing_human_agent.TypingHumanAgent()
    white_agent = random_agent.RandomAgent()
    # black_agent = random_agent.RandomAgent()
    black_agent = ai_agent.AIAgent()

    while not game_state.is_terminal():
        if game_state.get_player_to_move() == 1:
            action = white_agent.decide_action(game_state)
        else:
            action = black_agent.decide_action(game_state)

        try:
            game_state.take_action(action)
        except Exception as e:
            # print("oops, threw an exception!")
            print(e.args[0])
            game_state.print_board()
            game_state.print_sideboard()
            print(action.action_type)
            print(action.space)
            print(action.heading)
            print(action.piece_type)
            # input("press enter to continue")
            raise Exception(e)
        # game_state.take_action(action)
        if action.action_type == game.Game.Action.TYPE_END_TURN or action.action_type == game.Game.Action.TYPE_RESEARCH:
            turn_num += 1
            print(".")
            if turn_num % 30 == 0:
                game_state.print_board()

    if game_state.get_reward() > 0:
        print("White Wins!")
    if game_state.get_reward() < 0:
        print("Black Wins!")
    game_state.print_board()


if __name__ == "__main__":
    main()