from django.db import models


class Character(models.Model):
    name = models.CharField(max_length=30, default="player")
    image_url = models.CharField(max_length=250, default="")
    active = models.BooleanField(default=False)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'dungeon'
        db_table = 'dungeon_character'