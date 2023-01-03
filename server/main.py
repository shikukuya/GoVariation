import asyncio
from websockets.server import serve

async def handler(websocket, path):
    name = await websocket.recv()
    print(f"< {name}")
    greeting = f"Hello {name}!"
    await websocket.send(greeting)
    print(f"> {greeting}")

print("ws://0.0.0.0:34777/")
loop = asyncio.get_event_loop()
server = serve(handler, "0.0.0.0", 34777)
loop.run_until_complete(server)
loop.run_forever()
