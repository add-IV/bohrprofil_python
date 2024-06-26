from tkinter import *
from PIL import Image, ImageDraw, ImageFont
from os import path

from .bohrprofil import Bohrprofil, Layer

from .utils import get_pixels_per_cm


basedir = path.dirname(__file__)


def _get_bounds_xy(font: ImageFont, text: str) -> tuple[int, int]:
    bbox = font.getbbox(text)
    return bbox[2] + bbox[0], bbox[3] + bbox[1]


def _create_scale(draw: ImageDraw, max_depth: float):
    for i in range(int(max_depth) + 1):
        text = f"{i}.00 m"
        y = get_pixels_per_cm(i + 1)
        font = draw.getfont().font_variant(size=25)
        boundsxy = _get_bounds_xy(font, text)
        draw.text(
            (240 - boundsxy[0] - 5, y - boundsxy[1]),
            text,
            fill="black",
            font=font,
        )
        draw.line((80, y, 240, y), fill="black", width=3)


def _custom_resize(img: Image, height: int) -> Image:
    # repeats the image until the height is reached
    img_height = img.height
    img_width = img.width
    new_img = Image.new("RGB", (img_width, height))
    for y in range(0, height, img_height):
        new_img.paste(img, (0, y))
    return new_img


def _draw_textures(image: Image, layers: list[Layer]):
    start_y = get_pixels_per_cm(1)
    for layer in layers:
        y = get_pixels_per_cm(layer.end_depth + 1)
        texture = layer.texture
        img = Image.open(path.join(basedir, "..", "patterns", f"{texture}.png"))
        aspect_ratio = img.width / img.height
        img = img.resize((64, int(64 / aspect_ratio)))
        img = _custom_resize(img, int(y - start_y) + 1)
        image.paste(img, (400, int(start_y)))
        start_y = y


def _create_horizontal_lines(draw: ImageDraw, max_depth: float):
    draw.rectangle(
        (400, get_pixels_per_cm(1), 464, get_pixels_per_cm(max_depth + 1)),
        outline="black",
    )


def _create_switch_lines(
    draw: ImageDraw, layers: list[Layer], description_lines: list[float]
):
    draw.line((320, get_pixels_per_cm(1), 740, get_pixels_per_cm(1)), fill="black")
    font = draw.getfont().font_variant(size=15)
    for i, layer in enumerate(layers):
        text = f"{(layers[i].end_depth):.2f} m"
        boundsxy = _get_bounds_xy(font, text)
        draw.text(
            (320 + 5, get_pixels_per_cm(layers[i].end_depth + 1) - boundsxy[1]),
            text,
            font=font,
            fill="black",
        )
        draw.line(
            [
                320,
                get_pixels_per_cm(layers[i].end_depth + 1),
                500,
                get_pixels_per_cm(layers[i].end_depth + 1),
                540,
                description_lines[i],
                740,
                description_lines[i],
            ],
            fill="black",
        )


def _create_title(draw: ImageDraw, title: str):
    font = draw.getfont().font_variant(size=35)
    boundsxy = _get_bounds_xy(font, title)
    draw.text(
        (400 - boundsxy[0] // 2, 10),
        title,
        fill="black",
        font=draw.getfont().font_variant(size=35),
    )


def _create_descriptions(draw: ImageDraw, layers: list[Layer]) -> list[float]:
    description_lines = []
    font = draw.getfont().font_variant(size=15)
    current_y = get_pixels_per_cm(1)
    for layer in layers:
        current_y += 5
        boundsxy = _get_bounds_xy(font, layer.description)
        draw.text(
            (550, current_y),
            layer.description,
            fill="black",
            font=font,
        )
        current_y += boundsxy[1] + 5
        if current_y < get_pixels_per_cm(layer.end_depth + 1):
            current_y = get_pixels_per_cm(layer.end_depth + 1)
        description_lines.append(current_y)
    return description_lines


def _create_height(draw: ImageDraw, height: float):
    font = draw.getfont().font_variant(size=12)
    text = f"Meereshöhe: {height} m"
    boundsxy = _get_bounds_xy(font, text)
    draw.text(
        (320 + 5, get_pixels_per_cm(1) - boundsxy[1] - 5),
        text,
        fill="black",
        font=font,
    )


def draw_profile(bp: Bohrprofil) -> Image:
    image = Image.new(
        "RGB",
        (int(get_pixels_per_cm(7)), int(get_pixels_per_cm(bp.max_depth + 2))),
        "white",
    )
    draw = ImageDraw.Draw(image)
    draw.font = ImageFont.truetype("DejaVuSans.ttf", 15)
    _create_scale(draw, bp.max_depth)
    _draw_textures(image, bp.layers)
    _create_horizontal_lines(draw, bp.max_depth)
    _create_title(draw, bp.title)
    description_lines = _create_descriptions(draw, bp.layers)
    _create_switch_lines(draw, bp.layers, description_lines)
    _create_height(draw, bp.height)
    return image


if __name__ == "__main__":
    with open("bohrprofil.txt", "r") as file:
        bp = Bohrprofil.unmarshal(eval(file.read()))
    img = draw_profile(bp)
    img.save("bohrprofil.png")
