import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from websocket import create_connection
ws = create_connection("ws://localhost:8765")


def post_to_dict(post):
    dictionary = {}
    for k in post.keys():
        v = post[k]
        dictionary[k] = v
    return dictionary

def post_to_message_dict(post):
    msg = post_to_dict(post)
    if 'position[x]' in msg:
        msg['position'] = {
            'x': msg['position[x]'],
            'y': msg['position[y]']}
        del msg['position[x]']
        del msg['position[y]']
    if 'object[owner]' in msg:
        msg['object'] = {'owner': msg['object[owner]']}
        del msg['object[owner]']
    return msg

@csrf_exempt
def action(request):
    if request.method == "POST":
        msg = post_to_message_dict(request.POST)
        ws.send(json.dumps(msg).encode('utf8'))
    return HttpResponse("OK")

    # return HttpResponseBadRequest("Woops")