import random
from django.db import models
from dungeon.models.square import Square
from django.core.validators import MaxValueValidator, MinValueValidator


class Dungeon(models.Model):
    name = models.CharField(max_length=30)

    # room stats
    room_probability = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(1)])
    min_room_width = models.IntegerField()
    max_room_width = models.IntegerField()
    min_room_height = models.IntegerField()
    max_room_height = models.IntegerField()

    # tunnel stats
    min_tunnel_length = models.IntegerField()
    max_tunnel_length = models.IntegerField()
    tunnel_probability = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(1)])
    tunnel_entropy = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(1)])

    @property
    def squares(self):
        return Square.objects.filter(dungeon=self)

    def expand(self, x, y, radius):
        total_prob = self.room_probability + self.tunnel_probability
        can_expand = True
        while can_expand:
            endpoints = self.squares.filter(
                endpoint=True,
                x__gte=x-radius,
                x__lte=x+radius,
                y__gte=y-radius,
                y__lte=y+radius)
            can_expand = endpoints.exists()
            print("exploring %s endpoints in range of (%s, %s)" % (endpoints.count(), x, y))
            for endpoint in endpoints:
                if random.randint(0, total_prob) < self.tunnel_probability:
                    Square.objects.build_tunnel(
                        dungeon=self,
                        square=endpoint,
                        tunnel_length=random.randint(self.min_tunnel_length, self.max_tunnel_length))
                else:
                    Square.objects.build_room(
                        starting_square=endpoint,
                        width=random.randint(self.min_room_width, self.max_room_width),
                        height=random.randint(self.min_room_height, self.max_room_height))

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'dungeon'
        db_table = 'dungeon_dungeon'