
from utils import cheack_move_legality, broadcase_move
from utils import send_error_notification, check_if_game_over

## Maskes sure all the commands are in place
## Let us define an array that stores and communicates 
## all possibles states of our game

# Simple move parser
# takes a dictionary in the form of {'row': 3, 'col': 5}
# returns move in string
def board_parser(dict):
    position = str(chr(dict['col'] + 64)) + str(dict['row'])
    return position, dict['row'], dict['col']

def move_parcer(dict):
    number = dict['col'] * 10 + dict['row']

    if number == 11:
        return "TL"
    if number == 21:
        return "T"
    if number == 31:
        return "TR"
    if number == 12:
        return "L"
    if number == 32:
        return "R"
    if number == 13:
        return "BL"
    if number == 23:
        return "B"
    if number == 33:
        return "BR"
    else:
        return "Working on it"

# parsing game events
def game_update(event, session, player_id):
    board_pos_str, board_pos_row, board_pos_col = board_parser(event['boardPosition'])
    move_pos_str = move_parcer(event['movePosition'])
    print('before : ' + session.player_turn_state)
    taking_turns_state_machine(session, player_id, board_pos_str, move_pos_str)
    print('after : ' + session.player_turn_state)


# this function is the state machine for interchange of moves 
# between players. the state is stored in session object
def taking_turns_state_machine(session, player_id, board_pos_id, move_pos_id):
    if session.player_turn_state == 'player_0_turn':
        if player_id == 0:
            if not cheack_move_legality(board_pos_id, move_pos_id):
                send_error_notification(player_id)
            else:
                # now we are in state A
                session.player_turn_state = 'player_1_turn'
                # string for boradcasting the move
                str = board_pos_id + ' ' + move_pos_id # todo
                session.checkerboard.update_game_state(str)
                broadcase_move(session.socketlist, str)
                check_if_game_over()
    
    if session.player_turn_state == 'player_1_turn':
        if player_id == 1:
            if not cheack_move_legality(board_pos_id, move_pos_id):
                send_error_notification(player_id)
            else:
                # now we are in state A
                session.player_turn_state = 'player_0_turn'
                # string for boradcasting the move
                str = board_pos_id + ' ' + move_pos_id # todo
                session.checkerboard.update_game_state(str)
                broadcase_move(session.socketlist, str)
                check_if_game_over()


