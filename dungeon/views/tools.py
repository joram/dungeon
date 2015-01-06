from django.shortcuts import render_to_response
from dungeon.models import Dungeon, Square


def build_dungeon(request):
    print("building dungeon")
    # remove old dungeon
    Dungeon.objects.all().delete()
    Square.objects.all().delete()

    d = Dungeon.objects.create(
        name="Main Dungeon",
        min_room_width=3,
        max_room_width=10,
        min_room_height=3,
        max_room_height=10,
        min_tunnel_length=3,
        max_tunnel_length=15,
        tunnel_entropy=40,
        room_probability=30,
        tunnel_probability=70)
    Square.objects.create(dungeon=d, solid=False, endpoint=True, x=0, y=0)
    d.expand(0, 0, 20)
    print("dungeon squares: %s" % d.squares)
    context = {'dungeon': d}
    return render_to_response('dungeon.html', context)
