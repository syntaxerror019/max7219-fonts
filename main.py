import argparse
import os
import string
from renderer import load_font
from preview import preview_font
from exporter import export_header

def main():
    parser = argparse.ArgumentParser(description="MAX7219 Font Generator CLI")
    parser.add_argument("font", help="Path to the TTF or OTF font file")
    parser.add_argument("-s", "--size", type=int, default=8, help="Font size (default: 8)")
    parser.add_argument("-p", "--preview", action="store_true", help="Print a terminal preview of the font")
    parser.add_argument("-t", "--test", type=str, help="A specific string to preview")
    parser.add_argument("-e", "--export", type=str, help="Path to the output C++ header file (.h)")
    parser.add_argument("-n", "--name", type=str, help="Name of the font variable in C++ (defaults to export file name)")
    parser.add_argument("-c", "--chars", type=str, default=string.printable[:95], help="Characters to render (default: printable ASCII)")

    args = parser.parse_args()

    if not os.path.exists(args.font):
        print(f"Error: Font file '{args.font}' not found.")
        return

    print(f"Loading font '{args.font}' at size {args.size}...")
    font = load_font(args.font, size=args.size, chars=args.chars)
    print(f"Loaded {len(font)} characters.")

    if args.preview or args.test:
        test_str = args.test if args.test else args.chars
        preview_font(font, test_str)

    if args.export:
        font_name = args.name
        if not font_name:
            font_name = os.path.splitext(os.path.basename(args.export))[0]
            # Replace invalid C identifiers
            font_name = font_name.replace("-", "_").replace(" ", "_")
        
        export_header(font, args.export, font_name)

if __name__ == "__main__":
    main()
