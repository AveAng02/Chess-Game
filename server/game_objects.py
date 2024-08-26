
class player:
    def __init__(self, id, connection):
        self.id = id
        self.connection = connection


class checkerBoard:
    def __init__(self):
        # Initialize a 5x5 board with None representing empty spaces
        self.board = [["  " for _ in range(5)] for _ in range(5)]

    def get_current_state(self):
        return board

    def update_game_state(self, move_str):
        print('gamestate is updated with the move ' + move_str)


class session:
    def __init__(self, player, checkerboard):
        self.checkerboard = checkerboard
        self.playerlist = set()
        self.playerlist.add(player)
        self.socketlist = set()
        self.socketlist.add(player.connection)
        self.player_turn_state = 'player_0_turn'
        self.game_lifetime_state = 'continue_game'

        print(checkerboard.board)

    def add_player(self, player):
        self.playerlist.add(player)
        self.socketlist.add(player.connection)

    def remove_player(self, websocket):
        pass


# add user function