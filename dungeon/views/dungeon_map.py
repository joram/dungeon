from django.shortcuts import render_to_response
from dungeon.builder.dungeon_builder import DungeonBuilder


def grid_map(request):
    dungeon = DungeonBuilder(40)
    dungeon.run(
        num_rooms=50,
        min_room_width=3,
        max_room_width=10,
        min_room_height=3,
        max_room_height=10,
        num_tunnels=300,
        min_tunnel_length=3,
        max_tunnel_length=15)

    (min_x, max_y), (max_x, min_y) = dungeon.bounds()
    context = {
        'squares': dungeon.all_squares,
        'x_offset': min_x,
        'y_offset': min_y,
    }

    print(context)
    print(dungeon)

    return render_to_response('dungeon.html', context)