from django.shortcuts import render_to_response
from dungeon.models.dungeon_model import Dungeon


def dungeon(request):
    print("dungeon view")
    if Dungeon.objects.all().exists():
        context = {'dungeon': Dungeon.objects.all()[0]}
        return render_to_response('dungeon.html', context)