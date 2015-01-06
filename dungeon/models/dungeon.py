from django.db import models


class Dungeon(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'dungeon'
        db_table = '"dungeon_dungeon"'