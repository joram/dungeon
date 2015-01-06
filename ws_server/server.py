#!/usr/bin/python3
import json
from ws_server.base_server import BaseServerProtocol, run_server, get_clients


class DungeonProtocol(BaseServerProtocol):

    def onMessage(self, payload, _):
        message = json.loads(str(payload.decode('utf8')))
        print("received: %s" % message)
        print("action: %s" % message.get('action'))
        if message.get('action') == 'connect':
            self.send({'action': 'welcome', 'id': self.uuid})
            spawn_message = {
                'action': 'spawn',
                'position': {'x': 0, 'y': 0},
                'object': {
                    'type': "character",
                    'owner': self.uuid}
            }
            for client in get_clients():
                client.send(spawn_message)

        if message.get('action') == 'move_character':
            for client in get_clients():
                client.send(message)

if __name__ == '__main__':

    run_server(DungeonProtocol)
