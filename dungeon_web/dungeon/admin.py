from django.contrib import admin
from dungeon.models import *

admin.site.register(Dungeon, admin.ModelAdmin)
admin.site.register(Square, admin.ModelAdmin)
admin.site.register(Character, admin.ModelAdmin)