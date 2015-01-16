from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('dungeon.views',
    url(r'^dungeon/create/?$', 'tools.build_dungeon'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'dungeon_view.dungeon'),
)
