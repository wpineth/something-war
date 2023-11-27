class Game:
    ### RULES ###
    # The game is played on an 8x8 board, with 14 cities spread throughout.
    # B  .  o  .  .  .  .  o
    # .  .  .  .  o  .  .  .
    # o  .  o  .  .  .  .  .
    # .  .  .  .  .  .  o  .
    # .  o  .  .  .  .  .  .
    # .  .  .  .  .  o  .  o
    # .  .  .  o  .  .  .  .
    # o  .  .  .  .  o  .  W
    # Cities start out neutral (0) but can be taken over
    # At the beginning, the top left corner is controlled by Black and the bottom right by White

    # The game has 7 types of pieces. These are encoded as ±1-7, with positive being White and negative being Black
    # Each piece has several important statistics, listed below as a tuple (M, A, R, C):
    # M - Maximum Health
    # A - Attack Damage
    # R - Retaliation Damage
    # C - Cost

    # The Pieces are
    # 1 - Basic     - (2, 1, 1, 1) - No special abilities
    # 2 - Runner    - (1, 1, 0, 1) - Can move twice before attacking
    # 3 - Defender  - (3, 1, 3, 2) - When killed, the attacker takes one damage (unless ranged attack)
    # 4 - Swordsman - (3, 2, 1, 3) - No special abilities
    # 5 - Archer    - (2, 1, 0, 3) - Can attack two spaces away if it has no enemy neighbor in that direction
    # 6 - Support   - (2, 0, 1, 2) - Can bless an ally to give them +R and ignore next instance of damage
    # 7 - Berserker - (3, 2, 0, 4) - Can attack again after killing an enemy

    # Command Phase:
    # (Note: Adjacency is always defined to be the 8 spaces orthogonally or diagonally next to yours, like a chess king)
    # - At the beginning of a player's turn, all of their pieces get set to one point of move readiness and one point of
    #   attack readiness
    # - A piece may spend a point of move readiness to move one space into an adjacent unoccupied space
    # - If a piece is adjacent to an enemy piece, it may forfeit all of its move readiness and spend one point of
    #   attack readiness to attack the neighboring enemy piece (known as the victim)
    # - The victim of an attack loses health equal to the attacker's A value.
    # - If the victim is reduced to 0 health, it dies, and the attacker moves into the space previously occupied by the
    #   victim
    # - If the victim is not reduced to 0 health, the victim deals retaliation damage, causing the attacker to lose
    #   health equal to the victim's R value.
    # - If this reduces the attacker to 0 health, the attacker is taken off the board.

    # Special Rules:
    # - The Runner starts its turn with two points of move readiness. Each of these two moves must be made into an
    #   unoccupied space and both are forfeited when it attacks.
    # - When a unit kills a Defender, it takes one point of retaliation damage before moving to enter the Defender's
    #   previous position. This may kill the attacking unit, in which case both the Defender and the attacking unit are
    #   taken off the board
    # - When an Archer chooses which direction to attack in, if there is an adjacent enemy in that direction, the attack
    #   happens as normal. However, if the adjacent space in that direction is empty or contains an ally, and the next
    #   space after in that direction contains an enemy, the Archer performs a ranged attack. The victim loses health
    #   equal to the Archer's A value, and, whether this kills them or not, the Archer neither moves nor takes
    #   retaliation damage
    # - When a Support blesses a unit, it remains blessed until the next time it would lose health. When a blessed unit
    #   attacks another unit, if the victim would deal retaliation damage, the blessed unit instead takes no damage and
    #   stops being blessed. When a blessed unit is attacked, it loses no health, retaliates as though it had an R value
    #   one greater than it does, and then stops being blessed.
    # - When a Berserker attacks and kills an enemy unit, it gains one point of attack readiness. This can immediately
    #   be spent to attack another unit from its new position

    # Civilization Phase:
    # - Once the player cannot or does not want to move more pieces, they get a Civilization Phase. During this phase,
    #   the player can either take the Research or Economy action.
    # - Research: The player may research one new unit type among the ones they do not yet know how to make. Until the
    #   end of the game, they will be able to produce this unit in addition to the Basic unit and any other units they
    #   may have researched.
    # - Economy: The player gains money equal to the number of cities they control on the board. Then, they can spend
    #   money to place new units on unoccupied cities under their control. The total cost of the units placed is
    #   deducted from their money total, and any remainder is kept for the future.

    # After the Civilization Phase, the player's turn ends and the other player takes their turn.

    ### IMPLEMENTATION DETAILS ###
    # - The positions on the board are designated both by a tuple numbering their position in the array, and as a
    #   two-character square name like how squares are named in chess. The correspondence is as follows:
    #   - The Top Left corner of the map is (0,0) or "A8"
    #   - The Top Right corner of the map is (0,7) or "H8"
    #   - The Bottom Left corner of the map is (7,0) or "A1"
    #   - The Bottom Right corner of the map is (7,7) or "H1"

    def __init__(self):
        self._NAME_TO_NUMBER = {
            "basic": 1,
            "runner": 2,
            "defender": 3,
            "swordsman": 4,
            "archer": 5,
            "support": 6,
            "berserker": 7
        }
        self._M_MAP = {
            1: 2,
            2: 1,
            3: 3,
            4: 3,
            5: 2,
            6: 2,
            7: 3
        }
        self._A_MAP = {
            1: 1,
            2: 1,
            3: 1,
            4: 2,
            5: 1,
            6: 0,
            7: 2
        }
        self._R_MAP = {
            1: 1,
            2: 0,
            3: 3,
            4: 1,
            5: 0,
            6: 1,
            7: 0
        }
        self._C_MAP = {
            1: 1,
            2: 1,
            3: 2,
            4: 3,
            5: 3,
            6: 2,
            7: 4
        }

        # a space without a city is represented by None.
        # a Black city is -1, a White city is 1, and a neutral city is 0
        self._cities = [
            [-1, None, 0, None, None, None, None, 0],
            [None, None, None, None, 0, None, None, None],
            [0, None, 0, None, None, None, None, None],
            [None, None, None, None, None, None, 0, None],
            [None, 0, None, None, None, None, None, None],
            [None, None, None, None, None, 0, None, 0],
            [None, None, None, 0, None, None, None, None],
            [0, None, None, None, None, 0, None, 1],
        ]

        # a Black piece is a negative number, a White piece is a positive number, and the magnitude tells you what kind
        # of piece it is. 0 means the space is unoccupied.
        self._pieces = [
            [-1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1]
        ]

        # The Max health of a piece can be determined by its type in self.pieces. This tracks each piece's current
        # health
        self._piece_health = [
            [2, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 2]
        ]

        # White plays first and their starting piece has one point of move and one point of attack readiness. Black will
        # get readiness at the start of their turn
        self._move_ready = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1]
        ]
        self._attack_ready = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1]
        ]

        # Nobody starts blessed
        self._bless = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]

        # player_to_move = 1 for white or -1 for black
        self._player_to_move = 1
        self._economy_phase = False

        # Black starts with one money to compensate for the disadvantage of going second.
        self._white_money = 0
        self._black_money = 1

        # There is no unit type 0. Both players start only able to build units of type 1 (Basic)
        self._white_research = {
            1: True,
            2: False,
            3: False,
            4: False,
            5: False,
            6: False,
            7: False,
        }
        self._black_research = {
            1: True,
            2: False,
            3: False,
            4: False,
            5: False,
            6: False,
            7: False,
        }

    def get_cities(self):
        return self._cities.copy()

    def get_pieces(self):
        return self._pieces.copy()

    def get_piece_health(self):
        return self._piece_health.copy()

    def get_move_ready(self):
        return self._move_ready.copy()

    def get_attack_ready(self):
        return self._attack_ready.copy()

    def get_bless(self):
        return self._bless.copy()

    def get_white_money(self):
        return self._white_money

    def get_black_money(self):
        return self._black_money

    def get_white_research(self):
        return self._white_research.copy()

    def get_black_research(self):
        return self._black_research.copy()

    def get_player_to_move(self):
        return self._player_to_move

    def get_economy_phase(self):
        return self._economy_phase

    def stringify(self):
        """
        ┏━━━━━┳━━━━━┳━━━━━┳━━━━━┳━━━━━┳━━━━━┳━━━━━┳━━━━━┓
        ┃b2  ■┃     ┃    ◈┃     ┃     ┃     ┃     ┃    ◈┃
        ┣━━━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━┫
        ┃     ┃     ┃     ┃     ┃    ◈┃     ┃     ┃     ┃
        ┣━━━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━┫
        ┃    ◈┃     ┃    ◈┃     ┃     ┃     ┃     ┃     ┃
        ┣━━━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━┫
        ┃     ┃     ┃     ┃     ┃     ┃     ┃    ◈┃     ┃
        ┣━━━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━┫
        ┃     ┃    ◈┃     ┃     ┃     ┃     ┃     ┃     ┃
        ┣━━━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━┫
        ┃     ┃     ┃     ┃     ┃     ┃    ◈┃     ┃    ◈┃
        ┣━━━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━┫
        ┃     ┃     ┃     ┃    ◈┃     ┃     ┃     ┃     ┃
        ┣━━━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━┫
        ┃    ◈┃     ┃     ┃     ┃     ┃    ◈┃     ┃B2! □┃
        ┗━━━━━┻━━━━━┻━━━━━┻━━━━━┻━━━━━┻━━━━━┻━━━━━┻━━━━━┛
        """

        # I know this is hacky but all the less hacky solutions are less elegant and this is only used here anyway
        WHITE_PIECES = " BRDSAUZ"
        BLACK_PIECES = " brdsauz"

        def stringify_tile(row, col):
            tile_out = ""

            # Letter for piece type
            piece_type = self._pieces[row][col]
            if piece_type < 0:
                tile_out += BLACK_PIECES[-piece_type]
            else:
                tile_out += WHITE_PIECES[piece_type]

            # Number for piece health
            piece_health = self._piece_health[row][col]
            if piece_health == 0:
                tile_out += " "
            else:
                tile_out += str(self._piece_health[row][col])

            # Symbol for piece readiness
            if self._move_ready[row][col] == 2:
                readiness = "‼"
            elif self._move_ready[row][col] == 1:
                readiness = "!"
            elif self._attack_ready[row][col] == 1:
                readiness = "."
            else:
                readiness = " "

            # If a piece is blessed, it will have a * next to its health, and readiness is after that
            if self._bless[row][col]:
                tile_out += "*" + readiness
            else:
                tile_out += readiness + " "

            # Symbol for city control
            match self._cities[row][col]:
                case 0:
                    tile_out += "◈"
                case -1:
                    tile_out += "■"
                case 1:
                    tile_out += "□"
                case _:
                    tile_out += " "

            return tile_out

        def stringify_row(row):
            row_out = "┃"
            for col in range(8):
                row_out += stringify_tile(row, col) + "┃"
            return row_out + "\n"

        string = "┏━━━━━┳━━━━━┳━━━━━┳━━━━━┳━━━━━┳━━━━━┳━━━━━┳━━━━━┓\n"
        for row in range(7):
            string += stringify_row(row)
            string += "┣━━━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━┫\n"
        string += stringify_row(7)
        string += "┗━━━━━┻━━━━━┻━━━━━┻━━━━━┻━━━━━┻━━━━━┻━━━━━┻━━━━━┛"
        
        return string

    def print(self):
        print(stringify(self))

    # Takes a space, either as a string of length 2 (e.g. "C3") or a tuple (e.g. (5, 2))
    # and a heading direction, either as a string of length 1 or 2 (e.g. "N" "SW") or a tuple (e.g. (-1, 0) (1,-1))
    def move(self, space, heading):
        row, col, vertical_heading, horizontal_heading = self._parse_board_action(space, heading)

        target_row = row + vertical_heading
        target_col = col + horizontal_heading

        if target_row < 0 or target_row > 7 or target_col < 0 or target_col > 7:
            raise Exception("Target space was invalid: " + str(target_row) + " " + str(target_col))

        if self._pieces[target_row][target_col] != 0:
            raise Exception("Target space was occupied")

        if self._move_ready[row][col] < 1:
            raise Exception("Piece does not have move readiness (already moved this turn)")

        # put the piece in its new position
        self._replace_piece(target_row, target_col, row, col)
        # after the piece is faithfully copied, one point of move readiness is subtracted
        self._move_ready[target_row][target_col] -= 1
        # the old tile is now empty
        self._clear_tile(row, col)

    def attack(self, space, heading):
        row, col, vertical_heading, horizontal_heading = self._parse_board_action(space, heading)

        target_row = row + vertical_heading
        target_col = col + horizontal_heading

        if target_row < 0 or target_row > 7 or target_col < 0 or target_col > 7:
            raise Exception("Target space was invalid: " + str(target_row) + " " + str(target_col))

        if self._attack_ready[row][col] < 1:
            raise Exception("Piece does not have attack readiness (already attacked this turn)")

        attacker_type = abs(self._pieces[row][col])
        victim_type = abs(self._pieces[target_row][target_col])

        # If the piece and the player_to_move have the same sign, that means a player is trying to attack their own
        # piece. We can check this because their product will be positive,
        if self._pieces[target_row][target_col] * self._player_to_move >= 0:
            if attacker_type == 5:  # Archer
                # Archers trying to attack a space with no enemy should check further in that direction
                self._archer_attack(row, col, vertical_heading, horizontal_heading)
            if attacker_type == 6:  # Support
                # Supports trying to attack a space with no enemy might be trying to bless an ally
                self._support_attack(row, col, vertical_heading, horizontal_heading)
            else:
                raise Exception("Target space does not contain an enemy")

        attacker_A = self._A_MAP[attacker_type]
        victim_R = self._R_MAP[victim_type]

        if self._bless[target_row][target_col] == 1:  # if victim blessed
            self._attack_ready[row][col] = 0  # attacker has no more attack (even Berserker as it failed to kill)

            self._hit(target_row, target_col, attacker_A)  # victim will survive this because it's blessed
            self._hit(row, col, victim_R + 1)  # victim hits back with +1 to its R
        else:
            self._attack_ready[row][col] = 0  # attacker has no more attack

            kill = self._hit(target_row, target_col, attacker_A)

            if kill:
                if attacker_type == 7:  # Berserker
                    self._attack_ready[row][col] = 1
                if victim_type == 3:  # Defender
                    self._hit(row, col, 1)
                self._replace_piece(target_row, target_col, row, col)
                self._clear_tile(row, col)
            else:
                self._hit(row, col, victim_R)  # if no kill, victim retaliates

    @staticmethod
    def _parse_space(space):
        if isinstance(space, tuple):
            row, col = space
        elif isinstance(space, str):
            # the 1'th index contains a number. Larger number = higher = lower row
            row = 8 - int(space[1])
            # the 0th index contains a letter. Larger letter = further right = higher row
            col = ord(space[0].lower()) - ord('a')
        else:
            raise Exception("Space was in an invalid format: " + str(space))

        if row < 0 or row > 7 or col < 0 or col > 7:
            raise Exception("Space was invalid: " + str(row) + " " + str(col))

        return row, col

    @staticmethod
    def _parse_heading(heading):
        if isinstance(heading, tuple):
            vertical_heading, horizontal_heading = heading
            if vertical_heading == 0 and horizontal_heading == 0:
                raise Exception("Heading was (0, 0)")
            if vertical_heading < -1 or vertical_heading > 1 or horizontal_heading < -1 or horizontal_heading > 1:
                raise Exception("Heading had values with magnitude greater than 1")
        elif isinstance(heading, str):
            vertical_heading, horizontal_heading = (999, 999)  # Pycharm gets mad if I don't do this
            match heading:
                case "N":
                    vertical_heading, horizontal_heading = (-1, 0)
                case "NE":
                    vertical_heading, horizontal_heading = (-1, 1)
                case "E":
                    vertical_heading, horizontal_heading = (0, 1)
                case "SE":
                    vertical_heading, horizontal_heading = (1, 1)
                case "S":
                    vertical_heading, horizontal_heading = (1, 0)
                case "SW":
                    vertical_heading, horizontal_heading = (1, -1)
                case "W":
                    vertical_heading, horizontal_heading = (0, -1)
                case "NW":
                    vertical_heading, horizontal_heading = (-1, -1)
                case "_":
                    raise Exception("Heading string was invalid: " + heading)
        else:
            raise Exception("Heading was in an invalid format: " + str(heading))

        return vertical_heading, horizontal_heading

    def _parse_board_action(self, space, heading):
        row, col = self._parse_space(space)

        if self._pieces[row][col] == 0:
            raise Exception("Space was empty: " + str(row) + " " + str(col))

        if self._pieces[row][col] * self._player_to_move < 0:  # negative times positive makes negative
            raise Exception("Piece belongs to the other player: " + str(row) + " " + str(col))

        vertical_heading, horizontal_heading = self._parse_heading(heading)

        return row, col, vertical_heading, horizontal_heading

    # Faithfully copy the piece from current position to target position
    def _replace_piece(self, target_row, target_col, row, col):
        self._pieces[target_row][target_col] = self._pieces[row][col]
        self._piece_health[target_row][target_col] = self._piece_health[row][col]
        self._move_ready[target_row][target_col] = self._move_ready[row][col]
        self._attack_ready[target_row][target_col] = self._attack_ready[row][col]
        self._bless[target_row][target_col] = self._bless[row][col]

    # Removes a piece from position
    def _clear_tile(self, row, col):
        self._pieces[row][col] = 0
        self._piece_health[row][col] = 0
        self._move_ready[row][col] = 0
        self._attack_ready[row][col] = 0
        self._bless[row][col] = 0

    # Deals damage to a piece, and removes it if it dies. Returns a boolean telling you whether it died
    def _hit(self, row, col, damage):
        if self._bless[row][col] == 1:  # if blessed, it lives and stops being blessed
            self._bless[row][col] = 0
            return False

        # otherwise, it takes damage
        self._piece_health[row][col] -= damage

        if self._piece_health[row][col] <= 0:
            # if it's reduced to 0 or less, remove it from the board and indicate that it died
            self._clear_tile(row, col)
            return True
        else:
            # otherwise, indicate that it didn't die
            return False

    # Archer attacks in short range are handled by the normal attack code. This is for archers hitting at distance 2
    def _archer_attack(self, row, col, vertical_heading, horizontal_heading):
        target_row = row + 2 * vertical_heading
        target_col = col + 2 * horizontal_heading

        if target_row < 0 or target_row > 7 or target_col < 0 or target_col > 7:
            raise Exception("Target space was invalid: " + str(target_row) + " " + str(target_col))

        if self._pieces[target_row][target_col] * self._player_to_move >= 0:
            raise Exception("Target space does not contain an enemy")

        self._hit(target_row, target_col, self._A_MAP[5])

    def _support_attack(self, row, col, vertical_heading, horizontal_heading):
        target_row = row + vertical_heading
        target_col = col + horizontal_heading

        # not necessary to check because it is checked elsewhere already
        # if target_row < 0 or target_row > 7 or target_col < 0 or target_col > 7:
        #     raise Exception("Target space was invalid: " + str(target_row) + " " + str(target_col))

        if self._pieces[target_row][target_col] * self._player_to_move <= 0:
            raise Exception("Target space does not contain an ally")

        if self._bless[target_row][target_col] == 1:
            raise Exception("Target is already blessed")

        self._bless[target_row][target_col] = 1

    def research(self, piece_type):
        if self._economy_phase:
            raise Exception("Cannot Research during Economy Phase")

        if isinstance(piece_type, str):
            piece_type = self._NAME_TO_NUMBER[piece_type]

        if self._player_to_move == 1:
            if self._white_research[piece_type]:
                raise Exception("Unit type already researched")
            self._white_research[piece_type] = True
        else:
            if self._black_research[piece_type]:
                raise Exception("Unit type already researched")
            self._black_research[piece_type] = True

        self._unready()
        self.end_turn()

    def economy(self):
        if self._economy_phase:
            raise Exception("Already in the Economy Phase")

        self._economy_phase = True
        self._unready()

        income = 0

        for row in range(8):
            for col in range(8):
                if self._cities[row][col] == self._player_to_move:
                    income += 1

        if self._player_to_move == 1:
            self._white_money += income
        else:
            self._black_money += income

    def place(self, space, piece_type):
        if not self._economy_phase:
            raise Exception("Trying to place a piece while not in the Economy Phase")

        row, col = self._parse_space(space)

        if self._cities[row][col] != self._player_to_move:
            raise Exception("Trying to place a piece in at a location that is not one of your cities")

        if self._pieces[row][col] != 0:
            raise Exception("Trying to place a piece in an occupied city")

        if isinstance(piece_type, str):
            piece_type = self._NAME_TO_NUMBER[piece_type]

        if self._player_to_move == 1:
            research = self._white_research
            money = self._white_money
        else:
            research = self._black_research
            money = self._black_money

        if not research[piece_type]:
            raise Exception("Trying to place a piece you haven't researched")

        cost = self._C_MAP[piece_type]
        if money < cost:
            raise Exception("You cannot afford this unit")

        if self._player_to_move == 1:
            self._white_money -= cost
        else:
            self._black_money -= cost

        self._pieces[row][col] = self._player_to_move * piece_type

    def end_turn(self):
        self._player_to_move *= -1
        self._economy_phase = False
        self._ready()

    def _unready(self):
        for row in range(8):
            for col in range(8):
                self._move_ready[row][col] = 0
                self._attack_ready[row][col] = 0

    def _ready(self):
        for row in range(8):
            for col in range(8):
                if self._pieces[row][col] * self._player_to_move > 0:
                    if abs(self._pieces[row][col]) == 2:  # Runner
                        self._move_ready[row][col] = 2
                    else:
                        self._move_ready[row][col] = 1
                    self._attack_ready[row][col] = 1
