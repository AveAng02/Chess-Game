import json
import asyncio
import websockets

async def handle_connection(websocket, path):
    async for message in websocket:
        # Check if the message is empty
        if not message.strip():
            # Handle empty message (e.g., log a message)
            print("Received empty message")
            continue

        print(message)
        await websocket.send(json.dumps({'text': 'Server received your message'}))

async def main():
    async with websockets.serve(handle_connection, 'localhost', 8080):
        await asyncio.Future()  # Run forever

if __name__ == '__main__':
    asyncio.run(main())