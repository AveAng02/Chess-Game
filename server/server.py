import json
import asyncio
import websockets

async def handle_connection(websocket, path):
    async for message in websocket:
        data = json.loads(message)
        print(f"Received message: {data['text']}")
        await websocket.send(json.dumps({'text': 'Server received your message'}))

async def main():
    async with websockets.serve(handle_connection, 'localhost', 8000):
        await asyncio.Future()  # Run forever

if __name__ == '__main__':
    asyncio.run(main())