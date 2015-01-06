import random
from dungeon.builder import DIRECTIONS
from square import Square
from dungeon.templatetags.square_image import square_image


class BaseBuilder():

    def __init__(self):
        self.squares = {}

    def set_square(self, point, **kargs):
        square = self.squares.get(point, Square())
        square.set(**kargs)
        self.squares[point] = square

    def solid(self, point):
        if point not in self.squares:
            return True
        if self.squares[point].solid:
            return True

    def endpoints(self):
        valid_endoints = []
        for point in self.squares:
            if self.squares[point].endpoint:
                if not self.squares[point].deadend:
                    valid_endoints.append(point)
        random.shuffle(valid_endoints)
        return valid_endoints

    def bounds(self):
        min_x = 0
        min_y = 0
        max_x = 0
        max_y = 0
        for (x, y) in self.squares:
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)
        return (min_x-1, max_y+1), (max_x+1, min_y-1)

    @property
    def all_squares(self):
        data = []
        (min_x, max_y), (max_x, min_y) = self.bounds()
        for x in range(min_x, max_x+1):
            for y in range(min_y, max_y+1):
                point = (x, y)
                square = self.squares[point] if point in self.squares else Square()
                data.append({
                    'x': x,
                    'y': y,
                    'img_url': square_image(square),
                    'square_type': 'solid' if square.solid else "empty"})
        return data

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

