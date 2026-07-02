from PIL import Image, ImageDraw, ImageFont
import string
from font import Font, Glyph

def render_character(ch, image_font, pixel_height=8):
    # Large temporary canvas
    img = Image.new("1", (64, 64), 0)
    draw = ImageDraw.Draw(img)

    draw.text((0, 0), ch, fill=1, font=image_font)

    bbox = img.getbbox()

    if bbox is None:
        return Image.new("1", (2, pixel_height), 0)

    glyph = img.crop(bbox)

    # Scale height to exactly 8 pixels
    w, h = glyph.size

    if h != pixel_height:
        new_w = max(1, round(w * pixel_height / h))
        glyph = glyph.resize((new_w, pixel_height), Image.NEAREST)

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

def load_font(font_path, size=8, chars=None):
    if chars is None:
        chars = string.printable[:95]  # ASCII 32-126
    
    image_font = ImageFont.truetype(font_path, size)
    font = Font()
    
    for ch in chars:
        img = render_character(ch, image_font, size)
        columns = image_to_columns(img)
        glyph = Glyph(
            character=ch,
            width=img.width,
            height=img.height,
            columns=columns
        )
        font.add(glyph)
        
    return font
