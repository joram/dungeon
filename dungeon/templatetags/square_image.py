import os
import random
from django import template

register = template.Library()

KEYWORDS = ['solid', 'empty', 'doorhorz', 'doorvert']
image_files = {}
base_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../")
img_dir = '%s/dungeon/static/images/tiles/' % base_dir
tile_imgs = os.listdir(img_dir)
for keyword in KEYWORDS:
    if keyword not in image_files:
        image_files[keyword] = []
    for img in tile_imgs:
        if keyword in img:
            image_files[keyword].append(img)

def _tile_image(name_contains="solid"):
    options = image_files.get(name_contains, [])
    if options:
        img = random.choice(options)
        return "/static/images/tiles/%s" % img


@register.simple_tag
def square_image(square):
    if square.door:
        return _tile_image("door%s" % square.door_type)
    if not square.solid:
        return _tile_image("empty")
    return _tile_image("solid")
