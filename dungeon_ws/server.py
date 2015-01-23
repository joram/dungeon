import json
import os
import time
import datetime
import threading
from base_server import BaseServerProtocol, run_server, get_clients
from dungeon.models import Character, Dungeon
from django.core.wsgi import get_wsgi_application
from dungeon.templatetags.square_image import square_js_object

os.environ['DJANGO_SETTINGS_MODULE'] = 'django.settings'
application = get_wsgi_application()

NOTIFY_SQUARES_DELTA_SECONDS = 1
TUNNEL_GENERATION_RADIUS = 30
NOTIFICATION_RADIUS = 20


class TunnelGenerationThread(threading.Thread):

    def run(self):
        while True:
            dungeon = Dungeon.objects.all()[0]
            characters = Character.objects.filter(active=True)
            for character in characters:
                dungeon.expand(character.x, character.y, TUNNEL_GENERATION_RADIUS, True)
            time.sleep(5)


class DungeonProtocol(BaseServerProtocol):

    def __init__(self):
        super(DungeonProtocol, self).__init__()
        self.character = None
        self.known_squares = []
        self.message_handlers = {
            'connect': self._connect,
            'move_character': self._move_character
        }
        self.last_notify_nearby_squares_at = None

    def _get_character(self):
        available_characters = Character.objects.filter(active=False)
        if available_characters.exists():
            self.character = available_characters[0]
            self.character.active = True
            self.character.save()

    def onMessage(self, payload, _):
        message = json.loads(str(payload.decode('utf8')))
        if 'action' in message:
            func = self.message_handlers.get(message.get('action'))
            if func:
                func(message)

    def _previously_unknown_squares(self, radius):
        dungeon = Dungeon.objects.all()[0]
        squares = dungeon.squares(x=self.character.x, y=self.character.y, radius=radius).filter(solid=False)
        for square in squares:
            if square.id not in self.known_squares:
                self.known_squares.append(square.id)
                yield square

    def _grouped_squares(self, radius=10, num=10):
        square_list = []
        for square in self._previously_unknown_squares(radius):
            square_list.append(square)
            if len(square_list) >= num:
                yield square_list
                square_list = []
        if square_list:
            yield square_list

    def notify_nearby_squares(self, radius):
        if self.character:
            now = datetime.datetime.now()
            prev = self.last_notify_nearby_squares_at
            if not prev or (now-prev).total_seconds() > NOTIFY_SQUARES_DELTA_SECONDS:
                self.last_notify_nearby_squares_at = now
                num_squares_notified = 0
                for squares_list in self._grouped_squares(radius=radius):
                    self.send({
                        'action': 'update_squares',
                        'squares': [square_js_object(s) for s in squares_list]})
                    num_squares_notified += len(squares_list)
                if num_squares_notified:
                    print("notified about %s squares" % num_squares_notified)

    def _connect(self, message):
        self._get_character()
        if self.character:

            # you spawn
            self.send({
                'action': 'welcome',
                'id': self.uuid,
                'position': {
                    'x': self.character.x,
                    'y': self.character.y},
                'object': {
                    'type': "character",
                    'owner': self.uuid,
                    'img_url': self.character.image_url}})
            self.notify_nearby_squares(radius=NOTIFICATION_RADIUS)

            # place already existing entities
            for other_client in get_clients(excluding=[self.uuid]):
                print("spawning already existing: %s" % other_client.uuid)
                spawn_message = {
                    'action': 'spawn',
                    'position': {
                        'x': other_client.character.x,
                        'y': other_client.character.y},
                    'object': {
                        'type': "character",
                        'owner': other_client.uuid,
                        'img_url': other_client.character.image_url}}
                self.send(spawn_message)

            # tell the others you've spawned
            spawn_message = {
                'action': 'spawn',
                'position': {
                    'x': self.character.x,
                    'y': self.character.y},
                'object': {
                    'type': "character",
                    'owner': self.uuid,
                    'img_url': self.character.image_url}}
            for client in get_clients():
                client.send(spawn_message)

    def _move_character(self, message):
        self.character.x = message.get('position', {}).get('x', 0)
        self.character.y = message.get('position', {}).get('y', 0)
        self.character.save()
        self.broadcast(message, ignoring=[self.uuid])
        self.notify_nearby_squares(radius=NOTIFICATION_RADIUS)

    def onClose(self, wasClean, code, reason):
        super(DungeonProtocol, self).onClose(wasClean, code, reason)
        self.character.active = False
        self.character.save()

        # tell the others you've despawned
        despawn_message = {
            'action': 'despawn',
            'position': {
                'x': self.character.x,
                'y': self.character.y},
            'object': {
                'type': "character",
                'owner': self.uuid,
                'img_url': self.character.image_url}}
        for client in get_clients():
            client.send(despawn_message)

if __name__ == '__main__':
    Character.objects.all().update(active=False)
    # dungeon_generator_thread = TunnelGenerationThread()
    # dungeon_generator_thread.start()

    run_server(DungeonProtocol)
