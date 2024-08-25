import asyncio
import json
import logging
import datetime
import random
from websockets.asyncio.server import broadcast, serve

logging.basicConfig()

# state values
USERS = set() # list of sockets attached
VALUE = [0, 'Some value here']

def users_event():
    return json.dumps({"type": "users", "count": len(USERS)})

def value_event():
    return json.dumps({"type": "value", "value": VALUE})

async def counter(websocket):
    global USERS, VALUE
    try:
        # Register user
        USERS.add(websocket)
        broadcast(USERS, users_event())
        # Send current state to user
        await websocket.send(value_event())
        # Manage state changes
        async for message in websocket:
            event = json.loads(message)
            if event["action"] == "minus":
                VALUE[0] -= 1
                VALUE[1] = "minus " + datetime.datetime.utcnow().isoformat()
                broadcast(USERS, value_event())
            elif event["action"] == "plus":
                VALUE[0] += 1
                VALUE[1] = "plus " + datetime.datetime.utcnow().isoformat()
                broadcast(USERS, value_event())
            else:
                logging.error("unsupported event: %s", event)

    finally:
        # Unregister user
        USERS.remove(websocket)
        broadcast(USERS, users_event())

async def main():
    async with serve(counter, "localhost", 6789):
        await asyncio.get_running_loop().create_future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())