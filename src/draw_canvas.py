from tkinter import *
from PIL import Image, ImageTk
from os import path

from .bohrprofil import Bohrprofil, Layer

from .utils import get_pixels_per_cm


basedir = path.dirname(__file__)

images = []


def _create_scale(c: Canvas, max_depth: float):
    for i in range(int(max_depth) + 1):
        text = f"{i}.00 m"
        y = get_pixels_per_cm(i + 1)
        c.create_text(240, y, text=text, anchor="se", font=("TkDefaultFont ", 25))
        c.create_line(80, y, 240, y, fill="black", width=3)


def _custom_resize(img: Image, height: int) -> Image:
    # repeats the image until the height is reached
    img_height = img.height
    img_width = img.width
    new_img = Image.new("RGB", (img_width, height))
    for y in range(0, height, img_height):
        new_img.paste(img, (0, y))
    return new_img


def _draw_textures(c: Canvas, layers: list[Layer]):
    start_y = get_pixels_per_cm(1)
    global images
    images = []
    for layer in layers:
        y = get_pixels_per_cm(layer.end_depth + 1)
        texture = layer.texture
        img = Image.open(path.join(basedir, "..", "patterns", f"{texture}.png"))
        aspect_ratio = img.width / img.height
        img = img.resize((64, int(64 / aspect_ratio)))
        img = _custom_resize(img, int(y - start_y) + 1)
        img = ImageTk.PhotoImage(img)
        images.append(img)
        c.create_image(400, start_y, image=img, anchor="nw")
        start_y = y


def _create_horizontal_lines(c: Canvas, max_depth: float):
    c.create_line(
        400, get_pixels_per_cm(1), 400, get_pixels_per_cm(max_depth + 1), fill="black"
    )
    c.create_line(
        464, get_pixels_per_cm(1), 464, get_pixels_per_cm(max_depth + 1), fill="black"
    )


def _create_switch_lines(
    c: Canvas, layers: list[Layer], description_lines: list[float]
):
    c.create_line(320, get_pixels_per_cm(1), 740, get_pixels_per_cm(1), fill="black")
    for i in range(len(layers)):
        c.create_text(
            320,
            get_pixels_per_cm(layers[i].end_depth + 1),
            text=f"{(layers[i].end_depth):.2f} m",
            anchor="sw",
            font=("TkDefaultFont ", 15),
        )
        c.create_line(
            320,
            get_pixels_per_cm(layers[i].end_depth + 1),
            500,
            get_pixels_per_cm(layers[i].end_depth + 1),
            fill="black",
        )
        c.create_line(
            500,
            get_pixels_per_cm(layers[i].end_depth + 1),
            540,
            description_lines[i],
            fill="black",
        )
        c.create_line(
            540, description_lines[i], 740, description_lines[i], fill="black"
        )


def _create_descriptions(c: Canvas, layers: list[Layer]):
    description_lines = []
    current_y = get_pixels_per_cm(1)
    for i in range(len(layers)):
        description = layers[i].description
        created_text = c.create_text(
            550,
            current_y + 10,
            text=description,
            anchor="nw",
            font=("TkDefaultFont ", 15),
            width=200 - 5,
        )
        bounds_bottom = c.bbox(created_text)[3]
        current_y = bounds_bottom - 10
        if current_y < get_pixels_per_cm(layers[i].end_depth + 1):
            current_y = get_pixels_per_cm(layers[i].end_depth + 1)
        description_lines.append(current_y)
    return description_lines


def _create_title(c: Canvas, title: str):
    c.create_text(
        get_pixels_per_cm(3.5), 20, text=title, anchor="n", font=("TkDefaultFont ", 35)
    )


def _create_height(c: Canvas, height: float):
    c.create_text(
        320,
        get_pixels_per_cm(1),
        text=f"Meereshöhe {height} m NN",
        anchor="sw",
        font=("TkDefaultFont ", 12),
    )


def draw_profile(c: Canvas, bp: Bohrprofil, max_height: int = 800):
    c.delete("all")
    c.config(
        width=get_pixels_per_cm(7),
        height=max_height,
        background="white",
        scrollregion=(
            0,
            0,
            int(get_pixels_per_cm(7)),
            int(get_pixels_per_cm(bp.max_depth + 3)),
        ),
    )
    _create_scale(c, bp.max_depth)
    _draw_textures(c, bp.layers)
    _create_horizontal_lines(c, bp.max_depth)
    _create_title(c, bp.title)
    description_lines = _create_descriptions(c, bp.layers)
    _create_switch_lines(c, bp.layers, description_lines)
    _create_height(c, bp.height)


if __name__ == "__main__":
    root = Tk()
    root.title("Bohrprofil")
    root.minsize(1400, 800)
    root.geometry("1400x800")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    frame = Frame(root)
    frame.grid(row=0, column=0, sticky=(N, W, E, S))
    canvas = Canvas(frame, width=get_pixels_per_cm(7), height=800, background="white")
    canvas.grid(row=0, column=0, sticky=(N, W, E, S))
    with open("bohrprofil.txt", "r") as file:
        bp = Bohrprofil.unmarshal(eval(file.read()))
    draw_profile(canvas, bp)
    root.mainloop()
