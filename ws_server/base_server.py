import uuid
import json
import time
import threading
import asyncio
import psycopg2
from autobahn.asyncio.websocket import WebSocketServerProtocol, WebSocketServerFactory

ws_clients = []


def get_clients(excluding=None):
    global ws_clients
    if excluding:
        return [client for client in ws_clients if client.uuid not in excluding]
    return ws_clients


class WSMessageSender(threading.Thread):

    def run(self):
        while True:
            for ws in ws_clients:
                while ws.messages:
                    msg = ws.messages.pop(0)
                    payload = json.dumps(msg).encode('utf8')
                    ws.sendMessage(payload, False)
                    time.sleep(0)


class BaseServerProtocol(WebSocketServerProtocol):

    def __init__(self):
        WebSocketServerProtocol.__init__(self)
        self.closed = False
        self.uuid = str(uuid.uuid4())
        self.messages = []

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")
        ws_clients.append(self)

    def onMessage(self, payload, _):
        message = json.loads(str(payload.decode('utf8')))
        print("received: %s" % message)

    def broadcast(self, payload, ignoring=None):
        for client in get_clients():
            send = True
            if ignoring and client.uuid in ignoring:
                send = False
            if send:
                client.send(payload)

    def send(self, payload):
        self.messages.append(payload)

    def onClose(self, wasClean, code, reason):
        global ws_clients
        print("WebSocket connection closed: {0}".format(reason))
        self.closed = True
        if self in ws_clients:
            ws_clients.remove(self)



def run_server(server_protocol, port=8765):

    ws_sender = WSMessageSender()
    ws_sender.start()

    factory = WebSocketServerFactory("ws://192.168.1.162", externalPort=port, debug=False)
    factory.protocol = server_protocol
    loop = asyncio.get_event_loop()
    coro = loop.create_server(factory, '0.0.0.0', port)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.close()