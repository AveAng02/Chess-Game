
class piece:
    def __init__(self, id, row, col):
        self.id = id
        self.row = row
        self.col = col

    def get_current_pos(self):
        return self.row, self.col

    def set_new_pos(self, row, col):
        self.row = row
        self.col = col

    def is_at(self, row, col):
        if self.row == row and self.col == col:
            return True
        return False

class pawn(piece):
    def __init__(self, id, row, col):
        super().__init__(id, row, col)
        self.name = 'P' + str(id)

    def update_pos(self, command):
        if command == 'F':
            self.row = self.row - 1
        elif command == 'B':
            self.row = self.row + 1
        elif command == 'L':
            self.col = self.col - 1
        elif command == 'R':
            self.col = self.col + 1

    def is_possible_move(self, command):
        if command == 'F':
            temp_row = self.row - 1
            temp_col = self.col
        elif command == 'B':
            temp_row = self.row + 1
            temp_col = self.col
        elif command == 'L':
            temp_row = self.row
            temp_col = self.col - 1
        elif command == 'R':
            temp_row = self.row
            temp_col = self.col + 1
        else:
            return False

        # checking if move is possible
        print(temp_row)
        print(temp_col)
        if temp_col in range(1, 6) and temp_row in range(1, 6):
            return True
        else:
            return False

class hero1(piece):
    def __init__(self, id, row, col):
        super().__init__(id, row, col)
        self.name = 'H1' + str(id)

    def update_pos(self, command):
        if command == 'F':
            self.row = self.row - 2
        elif command == 'B':
            self.row = self.row + 2
        elif command == 'L':
            self.col = self.col - 2
        elif command == 'R':
            self.col = self.col + 2


    def is_possible_move(self, command):
        if command == 'F':
            temp_row = self.row - 2
            temp_col = self.col
        elif command == 'B':
            temp_row = self.row + 2
            temp_col = self.col
        elif command == 'L':
            temp_row = self.row
            temp_col = self.col - 2
        elif command == 'R':
            temp_row = self.row
            temp_col = self.col + 2
        else:
            return False

        # checking if move is possible
        print(temp_row)
        print(temp_col)
        if temp_col in range(1, 6) and temp_row in range(1, 6):
            return True
        else:
            return False

class hero2(piece):
    def __init__(self, id, row, col):
        super().__init__(id, row, col)
        self.name = 'H2' + str(id)

    def update_pos(self, command):
        if command == 'FL':
            self.row = self.row - 2
            self.col = self.col - 2
        elif command == 'FR':
            self.row = self.row - 2
            self.col = self.col + 2
        elif command == 'BL':
            self.row = self.row + 2
            self.col = self.col - 2
        elif command == 'BR':
            self.row = self.row + 2
            self.col = self.col + 2

    def is_possible_move(self, command):
        if command == 'FL':
            temp_row = self.row - 2
            temp_col = self.col - 2
        elif command == 'FR':
            temp_row = self.row - 2
            temp_col = self.col + 2
        elif command == 'BL':
            temp_row = self.row + 2
            temp_col = self.col - 2
        elif command == 'BR':
            temp_row = self.row + 2
            temp_col = self.col + 2
        else:
            return False

        # checking if move is possible
        print(temp_row)
        print(temp_col)
        if temp_col in range(1, 6) and temp_row in range(1, 6):
            return True
        else:
            return False

class player:
    def __init__(self, id = None, connection = None):
        self.id = id
        self.connection = connection
        self.piecelist = []

    def add_piece(self, new_piece):
        self.piecelist.append(new_piece)

    def remove_piece(self, piece_id):
        for p in piecelist:
            if p.id == piece_id:
                piecelist.remove(p)

    def is_possible_move(self, row, col, command):
        for pc in self.piecelist:
            if pc.is_at(row, col):
                return pc.is_possible_move(command)
        return False
        

class checkerBoard:
    def __init__(self):
        # Initialize a 5x5 board with None representing empty spaces
        self.board = [['00' for _ in range(5)] for _ in range(5)]

    def addPlayer0(self, player):
        for i in range(0, 5):
            self.board[0][i] = player.piecelist[i].name

    def addPlayer1(self, player):
        for i in range(0, 5):
            self.board[4][i] = player.piecelist[i].name

    def get_current_state(self):
        return board

    def update_game_state(self, move_str):
        print('gamestate is updated with the move ' + move_str)

    def print_board(self):
        for cells in self.board:
            for i in cells:
                print(i, end = ' ')
            print('')


class session:
    def __init__(self, player, checkerboard):
        # adding pieces to player
        player.piecelist.append(pawn(1, 1, 1))
        player.piecelist.append(hero1(1, 1, 2))
        player.piecelist.append(hero2(1, 1, 3))
        player.piecelist.append(pawn(2, 1, 4))
        player.piecelist.append(pawn(3, 1, 5))
        # adding a board to the session
        self.checkerboard = checkerboard
        # ading player 0 to session
        self.playerlist = set()
        self.playerlist.add(player)
        self.socketlist = set()
        self.socketlist.add(player.connection)
        # adding player 0 to checkerboard
        self.checkerboard.addPlayer0(player)
        self.player_turn_state = 'player_0_turn'
        self.game_lifetime_state = 'waiting_for_player_1'
        print(self.game_lifetime_state)
        self.checkerboard.print_board()

    def add_player(self, player):
        # adding peices to player 1
        player.piecelist.append(pawn(1, 5, 1))
        player.piecelist.append(hero1(1, 5, 2))
        player.piecelist.append(hero2(1, 5, 3))
        player.piecelist.append(pawn(2, 5, 4))
        player.piecelist.append(pawn(3, 5, 5))
        # ading player 1 to session
        self.playerlist.add(player)
        self.socketlist.add(player.connection)
        # adding player 1 to checkerboard
        self.checkerboard.addPlayer1(player)
        self.game_lifetime_state = 'waiting_for_start_button'
        print(self.game_lifetime_state)
        self.checkerboard.print_board()

    def get_current_state(self):
        return board

    def update_game_state(self, move_str, player_id, command, board_pos_row, board_pos_col):
        player = list(self.playerlist)[player_id]
        row = 0
        col = 0

        for pc in player.piecelist:
            if pc.is_at(board_pos_row, board_pos_col):
                pc.update_pos(command)
                row, col = pc.get_current_pos()

        brd = self.checkerboard.board
        brd[row - 1][col - 1], brd[board_pos_row - 1][board_pos_col - 1] = brd[board_pos_row - 1][board_pos_col - 1], brd[row - 1][col - 1]

        print('gamestate is updated with the move ' + move_str) # todo

    def remove_player(self, websocket):
        pass


# add user function