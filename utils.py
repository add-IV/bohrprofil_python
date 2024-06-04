from glob import glob
from os import path


DPI = 300
PIXEL_PER_MM = DPI / 25.4
PIXEL_PER_CM = PIXEL_PER_MM * 10


def get_pixels_per_cm(cm: float):
    return cm * PIXEL_PER_CM

def get_textures():
    textures = []
    for file in glob("patterns/*.png"):
        textures.append(path.basename(file)[:-4])
    textures.sort()
    textures.sort(key=len)
    return textures

if __name__ == "__main__":
    print(get_textures())