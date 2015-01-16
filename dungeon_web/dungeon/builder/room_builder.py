import random
from dungeon.builder import add
from base_builder import BaseBuilder


class RoomBuilder(BaseBuilder):

    def __init__(self):
        BaseBuilder.__init__(self)
        self.blacklisted_room_endpoints = []

    def build_room(self, width, height, num_doors):
        for endpoint in self.endpoints():
            built = self.build_room_from_endpoint(width, height, num_doors, endpoint)
            if built:
                return True
        return False

    def _valid_starting_point(self, point, width, height, blocking_points):
        for x in range(point[0]-1, point[0]+width+2):
            for y in range(point[1]-1, point[1]+height+2):
                if (x, y) in blocking_points:
                    return False
        return True

    def _blocking_points(self, endpoint, width, height):
        (e_x, e_y) = endpoint
        blocking_points = []
        for x in range(e_x-height-1, e_x+height+2):
            for y in range(e_y-width-1, e_y+width+2):
                point = (x, y)
                if point in self.squares and not self.squares[point].solid:
                    if point != endpoint:
                        blocking_points.append(point)
        return blocking_points

    def _starting_point(self, endpoint, width, height, blocking_points):
        (e_x, e_y) = endpoint

        possible_starts = []
        for x in range(e_x-width+1, e_x+1):
            possible_starts.append((x, e_y-height))
            possible_starts.append((x, e_y+1))
        for y in range(e_y-height+1, e_y+1):
            possible_starts.append((e_x-width, y))
            possible_starts.append((e_x+1, y))
        random.shuffle(possible_starts)

        for starting_point in possible_starts:
            if self._valid_starting_point(starting_point, width, height, blocking_points):
                return starting_point

    def build_room_from_endpoint(self, width, height, num_doors, endpoint):
        blocking_points = self._blocking_points(endpoint, width, height)
        starting_point = self._starting_point(endpoint, width, height, blocking_points)
        if starting_point:
            (s_x, s_y) = starting_point
            for x in range(s_x, s_x+width):
                for y in range(s_y, s_y+height):
                    self.set_square((x, y), solid=False, room=True)

            built_doors = 0
            while built_doors < num_doors:
                bottom_right = (starting_point[0]+width-1, starting_point[1]+height-1)
                self._add_door_to_room(starting_point, bottom_right)
                built_doors += 1
            return True

    def _add_door_to_room(self, top_left, bottom_right):
        (tl_x, tl_y) = top_left
        (br_x, br_y) = bottom_right

        possible_doors = []
        for x in range(tl_x, br_x+1):
            possible_doors.append(((x, tl_y), (0, -1)))
            possible_doors.append(((x, br_y), (0, 1)))
        for y in range(tl_y, br_y+1):
            possible_doors.append(((tl_x, y), (-1, 0)))
            possible_doors.append(((br_x, y), (1, 0)))
        random.shuffle(possible_doors)

        for (from_point, direction) in possible_doors:
            #self.set_square(possible_door, marked=True)
            to_point = (from_point[0]+direction[0], from_point[1]+direction[1])
            if self.can_build_to(from_point, to_point):
                self.set_square(to_point, solid=False, endpoint=True, door=True)
                for (door_type, point1, point2) in [
                    ('horz', add(to_point, (1, 0)), add(to_point, (-1, 0))),
                    ('vert', add(to_point, (0, 1)), add(to_point, (0, -1)))]:
                    if self.solid(point1) and self.solid(point2):
                        self.set_square(to_point, door_type=door_type)
                return True
        return False

