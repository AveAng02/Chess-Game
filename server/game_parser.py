
from utils import cheack_move_legality, broadcase_move, broadcaset_board
from utils import send_error_notification, check_if_game_over

# takes a dictionary in the form of {'row': 3, 'col': 5}
def board_parser(dict):
    position = str(chr(dict['col'] + 64)) + str(dict['row'])
    return position, dict['row'], dict['col']

# takes a dictionary in the form of {'row': 3, 'col': 5}
def move_parcer(dict):
    number = dict['col'] * 10 + dict['row']

    if number == 11:
        return "FL"
    if number == 21:
        return "F"
    if number == 31:
        return "FR"
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
def json_parser(event, session, player_id):
    if session.game_lifetime_state != 'continue_game_subrouting':
        if event['event_type'] == 'session_life_event':
            game_progression_state_machine(session, event)
    else:
        if event['event_type'] == 'game_life_event':
            board_pos_str, board_pos_row, board_pos_col = board_parser(event['boardPosition'])
            move_pos_str = move_parcer(event['movePosition'])
            print('before : ' + session.player_turn_state)
            taking_turns_state_machine(session, player_id, board_pos_row, board_pos_col, board_pos_str, move_pos_str)
            print('after : ' + session.player_turn_state)


# this function is the state machine for interchange of moves 
# between players. the state is stored in session object
def taking_turns_state_machine(session, player_id, board_pos_row, board_pos_col, board_pos_id, move_pos_id):
    if session.player_turn_state == 'player_0_turn':
        if player_id == 0:
            if not cheack_move_legality(session, player_id, board_pos_row, board_pos_col, move_pos_id):
                send_error_notification(player_id)
            else:
                # now we are in state A
                session.player_turn_state = 'player_1_turn'
                # string for boradcasting the move
                str = board_pos_id + ' ' + move_pos_id # todo
                session.update_game_state(str, player_id, move_pos_id, board_pos_row, board_pos_col)
                session.checkerboard.print_board()
                broadcase_move(session.socketlist, str)
                broadcaset_board(session.socketlist, session.get_current_state())
                check_if_game_over(session)
    
    if session.player_turn_state == 'player_1_turn':
        if player_id == 1:
            if not cheack_move_legality(session, player_id, board_pos_row, board_pos_col, move_pos_id):
                send_error_notification(player_id)
            else:
                # now we are in state A
                session.player_turn_state = 'player_0_turn'
                # string for boradcasting the move
                str = board_pos_id + ' ' + move_pos_id # todo
                session.update_game_state(str, player_id, move_pos_id, board_pos_row, board_pos_col)
                session.checkerboard.print_board()
                broadcase_move(session.socketlist, str)
                broadcaset_board(session.socketlist, session.get_current_state())
                check_if_game_over(session)


def game_progression_state_machine(session, event):
    if session.game_lifetime_state == 'game_over':
        print('wait_for_start_button')
        session.game_lifetime_state = 'waiting_for_start_button'

    if session.game_lifetime_state == 'waiting_for_start_button':
        if event['action'] == 'start_game_button_pressed':
            print('continue_game_subrouting')
            session.game_lifetime_state = 'continue_game_subrouting'