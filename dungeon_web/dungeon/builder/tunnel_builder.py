import random
from base_builder import BaseBuilder
from dungeon.builder import DIRECTIONS


class TunnelBuilder(BaseBuilder):

    def __init__(self, tunnel_entropy=50):
        BaseBuilder.__init__(self)
        self.squares = {}
        self.tunnel_entropy = tunnel_entropy

    def random_valid_endpoint(self):

        for endpoint in self.endpoints():
            directions = list(DIRECTIONS)
            random.shuffle(directions)
            for direction in directions:
                next_point = endpoint[0]+direction[0], endpoint[1]+direction[1]
                if self.can_build_to(endpoint, next_point):
                    return endpoint, direction

        return None, None

    def build_new_tunnel(self, length):

        start_point, direction = self.random_valid_endpoint()
        if start_point:
            self.set_square(start_point, solid=False, endpoint=True)
            return self.build_tunnel(start_point, direction, length)

    def build_tunnel(self, current_point, direction, length):

        if length <= 0:
            self.set_square(current_point, endpoint=True)
            return current_point, True

        # turn
        forward_point = (current_point[0] + direction[0], current_point[1] + direction[1])
        need_to_turn = not self.can_build_to(current_point, forward_point)
        want_to_turn = random.randint(0, 100) < self.tunnel_entropy
        if need_to_turn or want_to_turn:
            possible_directions = list(DIRECTIONS)  # copy, don't share pointers
            back = -direction[0], -direction[1]
            possible_directions.remove(back)
            random.shuffle(possible_directions)

            while possible_directions:
                direction = possible_directions.pop()
                next_point = (current_point[0] + direction[0], current_point[1] + direction[1])
                if self.can_build_to(current_point, next_point):
                    self.set_square(next_point, solid=False)
                    return self.build_tunnel(next_point, direction, length-1)

        # straight
        if not need_to_turn:
            self.set_square(forward_point, solid=False)
            return self.build_tunnel(forward_point, direction, length-1)

        # stuck?
        self.set_square(current_point, deadend=True)
        return current_point, False

