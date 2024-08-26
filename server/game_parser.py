
## Maskes sure all the commands are in place
## Let us define an array that stores and communicates 
## all possibles states of our game

# Simple move parser
# takes a dictionary in the form of {'row': 3, 'col': 5}
# returns move in string
def move_parser(dict):
    position = str(chr(dict['col'] + 64)) + str(dict['row'])
    return position




