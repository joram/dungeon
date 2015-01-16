import os
from django.shortcuts import render_to_response
from django.conf import settings
from dungeon.models import Dungeon, Square, Character


def build_dungeon(request):

    print("building Dungeon")
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
    d.expand(0, 0, 10)
    context = {'dungeon': d}

    print("building Characters")
    Character.objects.all().delete()
    character_images_dir = os.path.join(settings.BASE_DIR, "dungeon/static/images/characters")
    files = [os.path.join(character_images_dir, f) for f in os.listdir(character_images_dir)]
    for filepath in files:
        Character.objects.create(
            name="Player %s" % files.index(filepath),
            image_url=filepath.replace(os.path.join(settings.BASE_DIR, "dungeon"), ""),
            x=0,
            y=0
        )

    return render_to_response('dungeon.html', context)
