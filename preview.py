from font import Font

def preview_font(font: Font, test_string: str = None):
    if test_string is None:
        test_string = "".join(sorted([g.character for g in font]))
    
    print()
    print("--- FONT PREVIEW ---")
    
    # We assume max height is 8 (or we can use max height from glyphs)
    max_h = max((g.height for g in font), default=8)
    
    for y in range(max_h):
        for ch in test_string:
            if ch not in font.glyphs:
                print("  " * 3, end="") # Placeholder for missing char
                continue
            
            glyph = font[ch]
            
            for x in range(glyph.width):
                # The column value holds the bit at y
                col = glyph.columns[x]
                if (col & (1 << y)):
                    print("██", end="")
                else:
                    print("  ", end="")
            
            # Space between characters
            print(" ", end="")
        print()
    print("--------------------")
    print()
