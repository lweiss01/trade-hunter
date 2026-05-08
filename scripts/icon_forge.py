import sys
import os
from pathlib import Path
from PIL import Image

def forge_icon(source_png, output_ico):
    print(f"--- Trade Hunter Icon Forge ---")
    print(f"Reading: {source_png}")
    
    if not os.path.exists(source_png):
        print(f"ERROR: Source icon not found at {source_png}")
        return False

    img = Image.open(source_png)
    
    # Standard Windows icon sizes
    sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    
    print(f"Generating multi-res icon: {sizes}")
    img.save(output_ico, format='ICO', sizes=sizes)
    
    print(f"SUCCESS: {output_ico} created.")
    return True

if __name__ == "__main__":
    SOURCE = r"C:\Users\lweis\Downloads\trade-hunter favicon_transparent_bg.png"
    OUTPUT = os.path.join(os.getcwd(), "trade-hunter.ico")
    
    if forge_icon(SOURCE, OUTPUT):
        sys.exit(0)
    sys.exit(1)
