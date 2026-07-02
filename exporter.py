import os
from font import Font

def export_header(font: Font, output_path: str, font_name: str = None):
    if font_name is None:
        # derive from path
        font_name = os.path.splitext(os.path.basename(output_path))[0]
        
    # We need to sort glyphs by ASCII character to ensure continuous offset mapping
    sorted_chars = sorted(font.glyphs.keys())
    if not sorted_chars:
        print("Error: No glyphs to export.")
        return
        
    start_char = ord(sorted_chars[0])
    end_char = ord(sorted_chars[-1])
    
    # Build data array and offset array
    data_bytes = []
    offsets = []
    current_offset = 0
    
    # Fill in any missing characters in the range with empty glyphs (width 0)
    for code in range(start_char, end_char + 1):
        ch = chr(code)
        offsets.append(current_offset)
        if ch in font.glyphs:
            glyph = font[ch]
            data_bytes.extend(glyph.columns)
            current_offset += glyph.width
            
    # Add final offset so the width of the last character can be calculated
    offsets.append(current_offset)
    
    # Format C arrays
    # 12 columns per line for hex dump
    def chunked_hex(bytes_list, chunk_size=12):
        lines = []
        for i in range(0, len(bytes_list), chunk_size):
            chunk = bytes_list[i:i+chunk_size]
            lines.append("    " + ", ".join(f"0x{b:02X}" for b in chunk) + ",")
        return "\n".join(lines)
        
    def chunked_int(int_list, chunk_size=12):
        lines = []
        for i in range(0, len(int_list), chunk_size):
            chunk = int_list[i:i+chunk_size]
            lines.append("    " + ", ".join(f"{n}" for n in chunk) + ",")
        return "\n".join(lines)

    header_content = f"""// Generated MAX7219 Font Header
// Font Name: {font_name}
// Character Range: ASCII {start_char} to {end_char}

#ifndef {font_name.upper()}_H
#define {font_name.upper()}_H

#include <avr/pgmspace.h>

const uint8_t {font_name}_data[] PROGMEM = {{
{chunked_hex(data_bytes)}
}};

//offset array contains the starting index of each character data in the array.
// To find the width of character:
// int width = {font_name}_offsets[c - {start_char} + 1] - {font_name}_offsets[c - {start_char}];
// Size is {len(offsets)} (number of characters + 1)
const uint16_t {font_name}_offsets[] PROGMEM = {{
{chunked_int(offsets)}
}};

const uint8_t {font_name}_start_char = {start_char};
const uint8_t {font_name}_end_char = {end_char};
const uint16_t {font_name}_data_size = {current_offset};

#endif // {font_name.upper()}_H
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(header_content)
    
    print(f"Exported {font_name} to {output_path}")
    print(f"Total data bytes: {current_offset}")
    print(f"Total offset bytes: {len(offsets) * 2}")
    print(f"Total memory usage: {current_offset + len(offsets) * 2} bytes")
