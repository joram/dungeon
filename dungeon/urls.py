from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('dungeon.views',
    url(r'^', 'dungeon_map.grid_map'),
    url(r'^dungeon/create', 'tools.build_dungeon'),
    url(r'^admin/', include(admin.site.urls)),
)
