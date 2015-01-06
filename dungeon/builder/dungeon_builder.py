import random
from dungeon.builder import DIRECTIONS, add
from dungeon.builder.square import Square
from dungeon.builder.room_builder import RoomBuilder
from dungeon.builder.tunnel_builder import TunnelBuilder


class DungeonBuilder(RoomBuilder, TunnelBuilder):

    def __init__(self, tunnel_entropy=50):
        TunnelBuilder.__init__(self, tunnel_entropy=tunnel_entropy)
        RoomBuilder.__init__(self)
        self.squares = {}
        self.tunnel_entropy = tunnel_entropy

    def run(self, num_rooms=5, num_tunnels=2, min_room_width=5, max_room_width=10, min_room_height=5, max_room_height=10, min_tunnel_length=20, max_tunnel_length=25, start_square=(0, 0)):
        self.set_square(start_square, solid=False, start=True, endpoint=True)

        tunnels_built = 0
        rooms_built = 0
        done_building_tunnels = False
        done_building_rooms = False
        while not (done_building_tunnels and done_building_rooms):
            done_building_tunnels = tunnels_built >= num_tunnels
            done_building_rooms = rooms_built >= num_rooms

            tunnels_todo = num_tunnels-tunnels_built
            rooms_todo = num_rooms-rooms_built
            total_actions_left = tunnels_todo + rooms_todo

            # Tunnels
            if not done_building_tunnels and random.randint(0, total_actions_left) < tunnels_todo:
                length = random.randint(min_tunnel_length, max_tunnel_length)
                self.build_new_tunnel(length)
                tunnels_built += 1

            # Rooms
            if not done_building_rooms and random.randint(0, total_actions_left) < rooms_todo:
                width = random.randint(min_room_width, max_room_width)
                height = random.randint(min_room_height, max_room_height)
                if self.build_room(width, height, 2):
                    rooms_built += 1

        # clean doors
        for point in self.squares:
            if self.squares[point].door:
                self.set_square(point, door=False, door_type=None)
                for (door_type, point1, point2) in [
                    ('horz', add(point, (1, 0)), add(point, (-1, 0))),
                    ('vert', add(point, (0, 1)), add(point, (0, -1)))]:
                    if self.solid(point1) and self.solid(point2):
                        self.set_square(point, door=True, door_type=door_type)

    def doublelist_squares(self):
        data = {}
        for point in self.squares:
            (x, y) = point
            square = self.squares[point]
            if x not in data:
                data[x] = {}
            data[x][y] = square
        return data

    def __str__(self):
        data = self.doublelist_squares()
        s = ""
        (min_x, max_y), (max_x, min_y) = self.bounds()
        for x in range(min_x, max_x+1):
            line = ""
            for y in range(min_y, max_y+1):
                square = data.get(x, {}).get(y, Square())
                line += square.short_str()
            s += "%s\n" % line
        return s