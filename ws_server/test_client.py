#!/usr/bin/python3.3

import asyncio
import websockets

@asyncio.coroutine
def hello():
    websocket = yield from websockets.connect('ws://localhost:8765/')
    name = '{"action": "chat"}'
    yield from websocket.send(name)
    while True:
        message = yield from websocket.recv()
        if not message:
            break
        print("received: %s" % message)

asyncio.get_event_loop().run_until_complete(hello())
