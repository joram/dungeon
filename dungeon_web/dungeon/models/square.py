import os
import random
import time
from django.db import models

DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]


KEYWORDS = ['solid', 'empty', 'doorhorz', 'doorvert']
image_files = {}
base_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../")
img_dir = '%s/dungeon/static/images/tiles/' % base_dir
tile_imgs = os.listdir(img_dir)
for keyword in KEYWORDS:
    if keyword not in image_files:
        image_files[keyword] = []
    for img in tile_imgs:
        if keyword in img:
            image_files[keyword].append(img)


def add(p1, p2):
    return p1[0]+p2[0], p1[1]+p2[1]


def _tile_image(name_contains="solid"):
    options = image_files.get(name_contains, [])
    if options:
        img = random.choice(options)
        return "/static/images/tiles/%s" % img


class BaseSquareManager(models.Manager):

    def solid(self, point):
        (x, y) = point
        if not self.filter(x=x, y=y).exists():
            return True
        return self.get(x=x, y=y).solid

    def can_build_to(self, from_point, to_point):

        points_to_check = [(to_point[0]+x, to_point[1]+y) for x in [-1, 0, 1] for y in [-1, 0, 1]]
        points_to_check.remove(from_point)
        for direction in DIRECTIONS:
            ignore_point = (from_point[0]+direction[0], from_point[1]+direction[1])
            if ignore_point in points_to_check:
                points_to_check.remove(ignore_point)
        points_to_check.append(to_point)

        for point in points_to_check:
            if not self.solid(point):
                return False
        return True

    def _carve(self, dungeon, point):
        square, _ = self.get_or_create(dungeon=dungeon, x=point[0], y=point[1])
        square.solid = False
        square.save()


class TunnelBuildingSquareManager(BaseSquareManager):

    def build_tunnel(self, dungeon, square, tunnel_length, sleep_lots=False):
        directions = list(DIRECTIONS)
        random.shuffle(directions)
        point = (square.x, square.y)
        for direction in directions:
            to_point = add(point, direction)
            if self.can_build_to(point, to_point):
                self.get_or_create(dungeon=dungeon, solid=False, endpoint=True, x=point[0], y=point[1])
            self._build_tunnel_recursive(dungeon, point, direction, tunnel_length, sleep_lots)

        # exhausted endpoint
        square.endpoint = False
        square.save()

    def _build_tunnel_recursive(self, dungeon, current_point, direction, tunnel_length, sleep_lots):

        if sleep_lots:
            time.sleep(0)

        if tunnel_length <= 0:
            self._carve(dungeon, current_point)
            self.filter(x=current_point[0], y=current_point[1]).update(endpoint=True)
            print("carved full tunnel")
            return current_point, True

        # turn
        forward_point = (current_point[0] + direction[0], current_point[1] + direction[1])
        need_to_turn = not self.can_build_to(current_point, forward_point)
        want_to_turn = random.randint(0, 100) < dungeon.tunnel_entropy
        if need_to_turn or want_to_turn:
            possible_directions = list(DIRECTIONS)  # copy, don't share pointers
            back = -direction[0], -direction[1]
            possible_directions.remove(back)
            random.shuffle(possible_directions)

            while possible_directions:
                direction = possible_directions.pop()
                next_point = (current_point[0] + direction[0], current_point[1] + direction[1])
                if self.can_build_to(current_point, next_point):
                    self._carve(dungeon, current_point)
                    return self._build_tunnel_recursive(dungeon, next_point, direction, tunnel_length-1, sleep_lots)

        # straight
        if not need_to_turn:
            self._carve(dungeon, current_point)
            return self._build_tunnel_recursive(dungeon, forward_point, direction, tunnel_length-1, sleep_lots)

        # stuck?
        self._carve(dungeon, current_point)
        return current_point, False


class RoomBuildingSquareManager(BaseSquareManager):

    def build_room(self, starting_square, width, height):
        top_left = (starting_square.x, starting_square.y)
        blocking_points = self._blocking_points(starting_square, width, height)
        starting_point = self._starting_point(top_left, width, height, blocking_points)
        if starting_point:
            (s_x, s_y) = starting_point
            for x in range(s_x, s_x+width):
                for y in range(s_y, s_y+height):
                    self._carve(starting_square.dungeon, (x, y))

            # built_doors = 0
            # while built_doors < starting_square.dungeon.num_doors:
            #     bottom_right = (starting_point[0]+width-1, starting_point[1]+height-1)
            #     self._add_door_to_room(starting_point, bottom_right)
            #     built_doors += 1
            # return True

        starting_square.endpoint = False
        starting_square.save()

    def _valid_starting_point(self, point, width, height, blocking_points):
        for x in range(point[0]-1, point[0]+width+2):
            for y in range(point[1]-1, point[1]+height+2):
                if (x, y) in blocking_points:
                    return False
        return True

    def _blocking_points(self, starting_square, width, height):
        blocking_squares = self.filter(
            solid=False,
            x__gte=starting_square.x-width,
            x__lte=starting_square.x+width,
            y__gte=starting_square.y-height,
            y__lte=starting_square.y+height)
        blocking_points = []
        for square in blocking_squares.exclude(id=starting_square.id):
            blocking_points.append((square.x, square.y))
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

    # def _add_door_to_room(self, top_left, bottom_right):
    #     (tl_x, tl_y) = top_left
    #     (br_x, br_y) = bottom_right
    #
    #     possible_doors = []
    #     for x in range(tl_x, br_x+1):
    #         possible_doors.append(((x, tl_y), (0, -1)))
    #         possible_doors.append(((x, br_y), (0, 1)))
    #     for y in range(tl_y, br_y+1):
    #         possible_doors.append(((tl_x, y), (-1, 0)))
    #         possible_doors.append(((br_x, y), (1, 0)))
    #     random.shuffle(possible_doors)
    #
    #     for (from_point, direction) in possible_doors:
    #         #self.set_square(possible_door, marked=True)
    #         to_point = (from_point[0]+direction[0], from_point[1]+direction[1])
    #         if self.can_build_to(from_point, to_point):
    #             self.set_square(to_point, solid=False, endpoint=True, door=True)
    #             for (door_type, point1, point2) in [
    #                 ('horz', add(to_point, (1, 0)), add(to_point, (-1, 0))),
    #                 ('vert', add(to_point, (0, 1)), add(to_point, (0, -1)))]:
    #                 if self.solid(point1) and self.solid(point2):
    #                     self.set_square(to_point, door_type=door_type)
    #             return True
    #     return False


class SquareManager(TunnelBuildingSquareManager, RoomBuildingSquareManager):
    pass


class Square(models.Model):

    SQUARE_TYPES = (
        ("W", 'Wall'),
        ("DH", 'Horizontal Door'),
        ("DV", 'Vertical Door'),
        ("P", 'Portal'))

    solid = models.BooleanField(default=True)
    endpoint = models.BooleanField(default=False)
    square_type = models.CharField(max_length=2, choices=SQUARE_TYPES, default="W")
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    dungeon = models.ForeignKey('dungeon.Dungeon')

    objects = SquareManager()

    @property
    def img_url(self):
        if self.solid:
            return _tile_image("solid")
        return _tile_image("empty")

    def __str__(self):
        return "(%s, %s) %s" % (self.x, self.y, self.solid)

    class Meta:
        app_label = 'dungeon'
        db_table = 'dungeon_square'
        unique_together = [('x', 'y')]