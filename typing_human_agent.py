from agent import *


class TypingHumanAgent(Agent):
    def decide_action(self, game_state):
        while(True):
            action_string = input("Your action: ")
            if action_string.lower() == "view":
                game_state.print_board()
                continue
            if action_string.lower() == "side":
                game_state.print_board()
                game_state.print_sideboard()
                continue
            if action_string.lower() == "help":
                print("Type \"view\" to see the board state")
                print("Type \"side\" to see the sideboard (research and money)")
                print("Moves are performed with the following syntax")
                print("ActionType [param1] [param2]")
                print("Parameters are either a space in Battleship notation, a compass direction, or an integer\n"
                      "corresponding to a piece type")
                print("Examples:")
                print("move H8 NW")
                print("attack G7 N")
                print("capture F3")
                print("research 2")
                print("economy")
                print("place F1 2")
                print("end")
                continue

            action_decomposition = action_string.split(" ")
            action_type_string = action_decomposition[0].lower()
            if action_type_string not in Game.Action.STRING_TO_TYPE:
                print("Try again (or type \"help\")")
                continue
            action_type = Game.Action.STRING_TO_TYPE[action_type_string]
            if len(action_decomposition) < self._num_parameters(action_type):
                print("Try again (or type \"help\")")
                continue

            action = Game.Action(action_type)

            match action_type:
                case Game.Action.TYPE_MOVE:
                    action.space = action_decomposition[1]
                    action.heading = action_decomposition[2]
                case Game.Action.TYPE_ATTACK:
                    action.space = action_decomposition[1]
                    action.heading = action_decomposition[2]
                case Game.Action.TYPE_CAPTURE:
                    action.space = action_decomposition[1]
                case Game.Action.TYPE_RESEARCH:
                    action.piece_type = int(action_decomposition[1])
                case Game.Action.TYPE_ECONOMY:
                    pass
                case Game.Action.TYPE_PLACE:
                    action.space = action_decomposition[1]
                    action.piece_type = int(action_decomposition[2])
                case Game.Action.TYPE_END_TURN:
                    pass
            print("Accepted")
            return action

    def _num_parameters(self, action_type):
        match action_type:
            case Game.Action.TYPE_MOVE:
                return 3
            case Game.Action.TYPE_ATTACK:
                return 3
            case Game.Action.TYPE_CAPTURE:
                return 2
            case Game.Action.TYPE_RESEARCH:
                return 2
            case Game.Action.TYPE_ECONOMY:
                return 1
            case Game.Action.TYPE_PLACE:
                return 3
            case Game.Action.TYPE_END_TURN:
                return 1