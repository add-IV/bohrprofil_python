from glob import glob
from os import path

basedir = path.dirname(__file__)

DPI = 300
PIXEL_PER_MM = DPI / 25.4
PIXEL_PER_CM = PIXEL_PER_MM * 10


def get_pixels_per_cm(cm: float):
    return cm * PIXEL_PER_CM

def get_textures():
    textures = []
    for file in glob("*.png", root_dir=path.join(basedir, "..", "patterns")):
        textures.append(path.basename(file)[:-4])
    textures.sort()
    return textures

def open_textures_dir():
    import os
    os.system(f"start {path.join(basedir, '..', 'patterns')}")

if __name__ == "__main__":
    print(get_textures())