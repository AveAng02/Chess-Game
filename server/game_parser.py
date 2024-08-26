
## Maskes sure all the commands are in place
## Let us define an array that stores and communicates 
## all possibles states of our game

# Simple move parser
# takes a dictionary in the form of {'row': 3, 'col': 5}
# returns move in string
def piece_parcer(dict):
    position = str(chr(dict['col'] + 64)) + str(dict['row'])
    return position

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
def game_update(event):
    if event["action"] == "board_button":
        return piece_parcer(event["position"])
        
    elif event["action"] == "move_button":
        return move_parcer(event["position"])

    else:
        logging.error("unsupported event: %s", event)
