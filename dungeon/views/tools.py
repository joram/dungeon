from django.http import HttpResponse
from django.shortcuts import render_to_response
from dungeon.builder.dungeon_builder import DungeonBuilder
from dungeon.models import Dungeon, Square


def build_dungeon(request):

    # remove old dungeon
    Dungeon.objects.all().delete()
    Square.objects.all().delete()

    dungeon_builder = DungeonBuilder(40)
    dungeon_builder.run(
        num_rooms=50,
        min_room_width=3,
        max_room_width=10,
        min_room_height=3,
        max_room_height=10,
        num_tunnels=300,
        min_tunnel_length=3,
        max_tunnel_length=15)

    dungeon = Dungeon.objects.create(name="Main Dungeon")
    for position in dungeon_builder.squares:
        (x, y) = position
        s = dungeon_builder.squares[position]
        Square.objects.create(
            dungeon=dungeon,
            x=x,
            y=y,
            solid=s.solid)

    return HttpResponse()