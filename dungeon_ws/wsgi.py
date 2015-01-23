"""
WSGI config for dungeon websocket project.
It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dungeon.settings")


def application(environ, start_response):
    Character.objects.all().update(active=False)
    run_server(DungeonProtocol)

