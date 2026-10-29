'''Preset Enterprise sprites for the seed page.

Each PNG in the enterprise_sprites folder becomes an option in the seed page's
Enterprise list, named after its file (rainbow_stripes.png is "Rainbow Stripes").
An artist to credit can follow the name after a double dash, written as they
want it shown (rainbow_stripes--Galeswift.png).
The PNGs use the format described in markdown/enterprise_sprite.md, and are
checked here with the same rules the page applies to an uploaded PNG, so a
broken one is logged and left out instead of reaching players.
'''

import base64
import io
import os

import cherrypy
from PIL import Image

SPRITES_DIR = os.path.join(os.path.dirname(__file__), 'enterprise_sprites')

PNG_WIDTH = 104
PNG_HEIGHT = 16
PALETTE_X = 96
PALETTE_Y = 8
FRAME_COUNT = 6


def load():
    '''Returns [{ 'name', 'artist', 'png' }] for every usable PNG, with 'png' as a
    data URL and 'artist' empty when the file doesn't name one.'''
    sprites = []
    if not os.path.isdir(SPRITES_DIR):
        return sprites

    for filename in sorted(os.listdir(SPRITES_DIR)):
        if not filename.lower().endswith('.png'):
            continue
        with open(os.path.join(SPRITES_DIR, filename), 'rb') as infile:
            data = infile.read()
        error = check(data)
        if error:
            cherrypy.log(f"Leaving out Enterprise sprite {filename}: {error}")
            continue
        name, _, artist = os.path.splitext(filename)[0].partition('--')
        sprites.append({
            'name' : name.replace('_', ' ').title(),
            'artist' : artist.strip(),
            'png' : 'data:image/png;base64,' + base64.b64encode(data).decode('ascii'),
        })
    return sprites


def check(data):
    '''Returns why the PNG can't be used, or None if it can.'''
    try:
        image = Image.open(io.BytesIO(data)).convert('RGBA')
    except Exception:
        return "it couldn't be read as an image"

    if image.size != (PNG_WIDTH, PNG_HEIGHT):
        return f"it must be {PNG_WIDTH}x{PNG_HEIGHT} pixels, not {image.size[0]}x{image.size[1]}"

    def get_pixel(x, y):
        r, g, b, a = image.getpixel((x, y))
        if a < 128:
            return None
        return (r & 0xF8, g & 0xF8, b & 0xF8)

    palette = []
    for index in range(16):
        x = PALETTE_X + (index % 4) * 2
        y = PALETTE_Y + (index // 4) * 2
        color = get_pixel(x, y)
        if color is None or any(get_pixel(x + dx, y + dy) != color for dx, dy in ((1, 0), (0, 1), (1, 1))):
            return f"color {index} in the palette block (at {x}, {y}) must be a solid 2x2 square"
        palette.append(color)

    for x in range(FRAME_COUNT * 16):
        for y in range(PNG_HEIGHT):
            color = get_pixel(x, y)
            if color is not None and color != palette[0] and color not in palette[1:]:
                return f"the pixel at {x}, {y} isn't in the palette block"

    return None
