from glob import glob
from os import path
import sys

basedir = path.dirname(__file__)

DPI = 300
PIXEL_PER_MM = DPI / 25.4
PIXEL_PER_CM = PIXEL_PER_MM * 10


def get_pixels_per_cm(cm: float):
    return cm * PIXEL_PER_CM


def get_external_dir():
    """Directory for user-editable files (patterns, config.ini) — next to the exe when frozen."""
    if getattr(sys, 'frozen', False):
        return path.dirname(sys.executable)
    return path.join(basedir, '..')


def get_bundle_dir():
    """Directory for read-only bundled files (font, icon) — sys._MEIPASS when frozen."""
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS  # type: ignore[attr-defined]
    return path.join(basedir, '..')


def get_textures():
    textures = []
    for file in glob("*.png", root_dir=path.join(get_external_dir(), "patterns")):
        textures.append(path.basename(file)[:-4])
    textures.sort()
    return textures

def open_textures_dir():
    import os
    os.system(f"start {path.join(get_external_dir(), 'patterns')}")

if __name__ == "__main__":
    print(get_textures())