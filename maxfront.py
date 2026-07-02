from PIL import Image, ImageDraw, ImageFont
import string

FONT_FILE = "fonts/eight-bit-dragon.otf"
PIXEL_HEIGHT = 8

font = ImageFont.truetype(FONT_FILE, PIXEL_HEIGHT)


def render_character(ch):

    # Large temporary canvas
    img = Image.new("1", (64, 64), 0)
    draw = ImageDraw.Draw(img)

    draw.text((0, 0), ch, fill=1, font=font)

    bbox = img.getbbox()

    if bbox is None:
        return Image.new("1", (2, PIXEL_HEIGHT), 0)

    glyph = img.crop(bbox)

    # Scale height to exactly 8 pixels
    w, h = glyph.size

    if h != PIXEL_HEIGHT:
        new_w = max(1, round(w * PIXEL_HEIGHT / h))
        glyph = glyph.resize((new_w, PIXEL_HEIGHT), Image.NEAREST)

    return glyph


def image_to_columns(img):

    w, h = img.size

    cols = []

    for x in range(w):

        value = 0

        for y in range(h):

            if img.getpixel((x, y)):
                value |= (1 << y)

        cols.append(value)

    return cols


glyphs = {}

for ch in string.printable[:95]:

    img = render_character(ch)

    glyphs[ch] = {
        "width": img.width,
        "height": img.height,
        "columns": image_to_columns(img)
    }

print("Loaded", len(glyphs), "glyphs")

print(glyphs["A"])

def preview(ch):

    img = render_character(ch)

    print()

    for y in range(img.height):

        for x in range(img.width):

            if img.getpixel((x, y)):
                print("██", end="")
            else:
                print("  ", end="")

        print()


preview("A")
preview("B")
preview("C")