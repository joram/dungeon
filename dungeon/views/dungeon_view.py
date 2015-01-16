from django.shortcuts import render_to_response
from dungeon.models import Dungeon


def dungeon(request):
    if Dungeon.objects.all().exists():
        context = {'dungeon': Dungeon.objects.all()[0]}
        return render_to_response('dungeon.html', context)