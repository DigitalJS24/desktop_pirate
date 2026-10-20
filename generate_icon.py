from PIL import Image
import os
from utils import get_asset_path

def create_ico():
    src_path = get_asset_path("sprites", "idle_right_0.png")
    dst_path = get_asset_path("icon.ico")
    if os.path.exists(src_path):
        img = Image.open(src_path)
        img.save(dst_path, format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
        print(f"Created {dst_path}")

if __name__ == "__main__":
    create_ico()

