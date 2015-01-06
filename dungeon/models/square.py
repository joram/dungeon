from django.db import models


class Square(models.Model):

    SQUARE_TYPES = (
        ("W", 'Wall'),
        ("DH", 'Horizontal Door'),
        ("DV", 'Vertical Door'),
        ("P", 'Portal'))

    solid = models.BooleanField(default=True)
    square_type = models.CharField(max_length=2, choices=SQUARE_TYPES, default="W")
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    dungeon = models.ForeignKey('dungeon')

    def __str__(self):
        return "(%s, %s) %s" % (self.x, self.y, self.square_type)

    class Meta:
        app_label = 'dungeon'
        db_table = '"dungeon_square"'
        unique_together = [('x', 'y')]