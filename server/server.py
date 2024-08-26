import asyncio
import json
import logging
import datetime
import random
from websockets.asyncio.server import broadcast, serve

from game_parser import piece_parcer, move_parcer, game_update

logging.basicConfig()

# state values
USERS = set() # list of sockets attached
VALUE = ['Some value here']

def users_event():
    return json.dumps({"type": "users", "count": len(USERS)})

def game_history_loggging_event():
    print('sending history')
    return json.dumps({"type": "game_history", "value": VALUE})

async def counter(websocket):
    global USERS, VALUE
    try:
        # Register 2 players only
        try:
            if len(USERS) < 2:
                USERS.add(websocket)
            else:
                websocket.send("Lobby is full.....")
        except Exception as e:
            print(f"An error occurred: {e}")

        broadcast(USERS, users_event())
        # Send current state to user
        await websocket.send(game_history_loggging_event())
        # Manage state changes
        async for message in websocket:
            event = json.loads(message)
            VALUE = game_update(event)
            broadcast(USERS, game_history_loggging_event())
            print(VALUE)

    finally:
        # Unregister user
        USERS.remove(websocket)
        broadcast(USERS, users_event())

async def main():
    async with serve(counter, "localhost", 6789):
        await asyncio.get_running_loop().create_future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())