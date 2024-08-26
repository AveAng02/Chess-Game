import asyncio
import json
import logging
import datetime
import random
from websockets.asyncio.server import broadcast, serve

from game_parser import game_update
from game_objects import checkerBoard, session, player

logging.basicConfig()

# state values
number_of_players = 0
USERS = [] # list of sockets attached
VALUE = ['Some value here']

def is_currect_user(websocket):
    for user in USERS:
        if websocket in user.socketlist:
            return True
    return False

def get_user_id(websocket):
    for i in range(len(USERS)):
        if websocket in USERS[i].socketlist:
            return i
    return -1

def users_event():
    return json.dumps({"type": "users", "count": len(USERS)})

def game_history_loggging_event():
    print('sending history')
    return json.dumps({"type": "game_history", "value": VALUE})

async def counter(websocket):
    global USERS, VALUE, number_of_players
    try:
        # making sure the connection is registered or not
        if not is_currect_user(websocket):
            # register the user if not registered
            print(number_of_players)
            # creating a new session with 2 users
            if number_of_players % 2 == 0:
                USERS.append(session(player(0, websocket), checkerBoard()))
            else:
                # add to the last session
                USERS[-1].add_player(player(1, websocket)) 
            
            number_of_players = number_of_players + 1
            print(len(USERS))
        
        # if registered
        temp_user_id = get_user_id(websocket)
        broadcast(USERS[temp_user_id].socketlist, users_event())
        # Send current state to user
        await websocket.send(game_history_loggging_event())
        # Manage state changes
        async for message in websocket:
            event = json.loads(message)
            print(event)
            VALUE = game_update(event)
            broadcast(USERS[temp_user_id].socketlist, game_history_loggging_event())
            print(VALUE)

    finally:
        # Unregister user
        # USERS.remove(websocket)
        # broadcast(USERS, users_event())
        print("Couldnot register user")

async def main():
    async with serve(counter, "localhost", 6789):
        await asyncio.get_running_loop().create_future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())