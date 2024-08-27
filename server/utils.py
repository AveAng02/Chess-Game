
import json
from websockets.asyncio.server import broadcast

# this check if the move is possible or legal in nature
def cheack_move_legality(session, player_id, board_pos_row, board_pos_col, command):
    # checks if piece is within bounds
    temp_player = list(session.playerlist)[player_id]
    state1 = temp_player.is_possible_move(board_pos_row, board_pos_col, command)
    
    # makes sure the target piece is not in the same team
    dest_row, dest_col = 0, 0
    if state1:
        # get's target pos
        for pc in temp_player.piecelist:
            if pc.is_at(board_pos_row, board_pos_col):
                pc.update_pos(command)
                dest_row, dest_col = pc.get_current_pos()
                pc.set_new_pos(board_pos_row, board_pos_col)
        
        # checks target pos for team member
        for pc in temp_player.piecelist:
            if pc.is_at(dest_row, dest_col):
                state1 = False

    return state1 # todo

def broadcase_move(sktlst, str):
    broadcast(sktlst, json.dumps({"type": "game_history", "value": str}))

def broadcaset_board(sktlst, str):
    print(str)
    broadcast(sktlst, json.dumps({"type": "board_update", "value": str}))

def send_error_notification(player_id):
    print('send error notification to ' + str(player_id))

def check_if_game_over(session):
    plrlst = list(session.playerlist)
    is_over = False

    if len(plrlst[0].piecelist) == 0:
        is_over = True
        peint('declare Player 1 as winner')
        session.game_lifetime_state = 'game_over'
    elif len(plrlst[1].piecelist) == 0:
        is_over = True
        peint('declare Player 0 as winner')
        session.game_lifetime_state = 'game_over'

    return is_over # todo
