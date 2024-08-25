import asyncio
import websockets

async def client():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        while True:
            message = input("Enter your message (or 'quit' to exit): ")
            if message.lower() == 'quit':
                break
            await websocket.send(message)
            print(f"Sent: {message}")
            response = await websocket.recv()
            print(f"Received: {response}")

async def main():
    await client()

if __name__ == "__main__":
    asyncio.run(main())