from tkinter import *
from PIL import Image, ImageTk

from bohrprofil import Bohrprofil, Layer

from utils import get_pixels_per_cm

images = []

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


def _custom_resize(img: Image, height: int) -> Image:
    # repeats the image until the height is reached
    img_height = img.height
    img_width = img.width
    new_img = Image.new("RGB", (img_width, height))
    for y in range(0, height, img_height):
        new_img.paste(img, (0, y))
    return new_img


def _draw_textures(c: Canvas, layers = list[Layer]):
    start_y = get_pixels_per_cm(1)
    global images
    images = []
    for layer in layers:
        y = get_pixels_per_cm(layer.end_depth+1)
        texture = layer.texture
        img = Image.open(f"patterns\\{texture}.png")
        aspect_ratio = img.width / img.height
        img = img.resize((64, int(64 / aspect_ratio)))
        img = _custom_resize(img, int(y - start_y))
        img = ImageTk.PhotoImage(img)
        images.append(img)
        c.create_image(400, start_y, image=img, anchor="nw")
        start_y = y


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
    _draw_textures(c, bp.layers)
    _create_horizontal_lines(c, bp.max_depth)
