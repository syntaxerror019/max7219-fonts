from dataclasses import dataclass

@dataclass
class Glyph:
    character: str
    width: int
    height: int
    columns: list[int]


class Font:
    def __init__(self):
        self.glyphs = {}

    def add(self, glyph: Glyph):
        self.glyphs[glyph.character] = glyph

    def __getitem__(self, c):
        return self.glyphs[c]

    def __iter__(self):
        return iter(self.glyphs.values())

    def __len__(self):
        return len(self.glyphs)