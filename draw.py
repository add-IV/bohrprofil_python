from tkinter import *


from bohrprofil import Bohrprofil, Layer

from utils import get_pixels_per_cm


def _create_scale(c: Canvas, max_depth: float):
    for i in range(int(max_depth) + 1):
        text = f"{i}.00 m"
        y = get_pixels_per_cm(i+1)
        created_text = c.create_text(0, 0, text=text, anchor="w", font=("TkDefaultFont ", 30))
        text_bbox = c.bbox(created_text)
        width = text_bbox[2] - text_bbox[0]
        height = text_bbox[3] - text_bbox[1]
        c.move(created_text, 240 - width, y - height / 2)
        c.create_line(80, y, 240, y, fill="black", width=3)


def _draw_textures():
    pass


def _create_horizontal_lines(c: Canvas, max_depth: float):
    c.create_line(400, get_pixels_per_cm(1), 400, get_pixels_per_cm(max_depth + 1), fill="black")
    c.create_line(464, get_pixels_per_cm(1), 464, get_pixels_per_cm(max_depth + 1), fill="black")



def _create_switch_lines():
    pass


def _create_descriptions():
    pass


def _create_title():
    pass


def _create_height():
    pass


def draw_profile(c: Canvas, bp: Bohrprofil):
    c.delete("all")
    c.config(
        width=get_pixels_per_cm(7),
        height=get_pixels_per_cm(bp.max_depth + 3),
        background="white",
    )
    _create_scale(c, bp.max_depth)
    _create_horizontal_lines(c, bp.max_depth)
