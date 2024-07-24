from tkinter import *
from PIL import Image, ImageDraw, ImageFont
from os import getcwd, path

from .bohrprofil import Bohrprofil, Layer
from .config import Config

from .utils import get_pixels_per_cm


def _get_bounds_xy(draw: ImageDraw, font: ImageFont, text: str) -> tuple[int, int]:
    bbox = draw.multiline_textbbox((0, 0), text, font=font)
    return bbox[2] + bbox[0], bbox[3] + bbox[1]


class BohrprofilDrawer:
    basedir = getcwd()

    def _create_scale(self, max_depth: float):
        for i in range(int(max_depth) + 1):
            text = f"{i}.00 m"
            y = get_pixels_per_cm(i) + self.config.get(
                "Abstände und Längen", "Erste Ebene Abstand"
            )
            font = self.draw.getfont().font_variant(size=25)
            start_x = self.config.get("Abstände und Längen", "Links Abstand")
            endx = self.config.get(
                "Abstände und Längen", "Links Abstand"
            ) + self.config.get("Abstände und Längen", "Maßstab Länge")
            boundsxy = _get_bounds_xy(self.draw, font, text)
            self.draw.text(
                (endx - boundsxy[0] - 5, y - boundsxy[1]),
                text,
                fill="black",
                font=font,
            )
            self.draw.line((start_x, y, endx, y), fill="black", width=3)

    def _custom_resize(self, img: Image, height: int) -> Image:
        # repeats the image until the height is reached
        img_height = img.height
        img_width = img.width
        new_img = Image.new("RGB", (img_width, height))
        for y in range(0, height, img_height):
            new_img.paste(img, (0, y))
        return new_img

    def _draw_textures(self, layers: list[Layer]):
        start_y = get_pixels_per_cm(1)
        image_width = self.config.get("Abstände und Längen", "Symbole Länge")
        start_x = (
            self.config.get("Abstände und Längen", "Links Abstand")
            + self.config.get("Abstände und Längen", "Maßstab Länge")
            + self.config.get("Abstände und Längen", "Mitte Abstand")
            + self.config.get("Abstände und Längen", "Schichtentiefe Länge")
        )
        for layer in layers:
            y = get_pixels_per_cm(layer.end_depth + 1)
            texture = layer.texture
            img = Image.open(path.join(self.basedir, "patterns", f"{texture}.png"))
            aspect_ratio = img.width / img.height
            img = img.resize((image_width, int(image_width / aspect_ratio)))
            img = self._custom_resize(img, int(y - start_y) + 1)
            self.image.paste(img, (start_x, int(start_y)))
            start_y = y

    def _create_horizontal_lines(self, max_depth: float):
        start_x = (
            self.config.get("Abstände und Längen", "Links Abstand")
            + self.config.get("Abstände und Längen", "Maßstab Länge")
            + self.config.get("Abstände und Längen", "Mitte Abstand")
            + self.config.get("Abstände und Längen", "Schichtentiefe Länge")
        )
        end_x = start_x + self.config.get("Abstände und Längen", "Symbole Länge")
        first_distance = self.config.get(
                "Abstände und Längen", "Erste Ebene Abstand"
            )
        self.draw.rectangle(
            (start_x, first_distance, end_x, get_pixels_per_cm(max_depth) + first_distance),
            outline="black",
            width=1,
        )

    def _create_switch_lines(self, layers: list[Layer], description_lines: list[float]):
        self.draw.line(
            (320, get_pixels_per_cm(1), 740, get_pixels_per_cm(1)),
            fill="black",
            width=1,
        )
        font = self.draw.getfont().font_variant(size=15)
        for i, layer in enumerate(layers):
            text = f"{(layers[i].end_depth):.2f} m"
            boundsxy = _get_bounds_xy(self.draw, font, text)
            self.draw.text(
                (320 + 5, get_pixels_per_cm(layers[i].end_depth + 1) - boundsxy[1]),
                text,
                font=font,
                fill="black",
            )
            self.draw.line(
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
                width=1,
            )

    def _create_title(self, title: str):
        font = self.draw.getfont().font_variant(size=35)
        boundsxy = _get_bounds_xy(self.draw, font, title)
        self.draw.text(
            (400 - boundsxy[0] // 2, 10),
            title,
            fill="black",
            font=font,
        )

    def _create_descriptions(self, layers: list[Layer]) -> list[float]:
        description_lines = []
        font = self.draw.getfont().font_variant(size=15)
        current_y = get_pixels_per_cm(1)
        for layer in layers:
            current_y += 5
            boundsxy = _get_bounds_xy(self.draw, font, layer.description)
            self.draw.text(
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

    def _create_height(self, height: float):
        font = self.draw.getfont().font_variant(size=12)
        text = f"Meereshöhe: {height} m"
        boundsxy = _get_bounds_xy(self.draw, font, text)
        self.draw.text(
            (320 + 5, get_pixels_per_cm(1) - boundsxy[1] - 5),
            text,
            fill="black",
            font=font,
        )

    def _new_image(self, width: int, height: int):
        self.image = Image.new(
            "RGB",
            (width, height),
            (255, 255, 255),
        )
        self.draw = ImageDraw.Draw(self.image)
        self.draw.font = ImageFont.truetype("DejaVuSans.ttf", 15)

    def draw_profile(self, bp: Bohrprofil, config: Config) -> Image:
        self._new_image(
            config.get_width(),
            int(get_pixels_per_cm(bp.max_depth) + config.get_extra_height()),
        )
        self.config = config
        self._create_scale(bp.max_depth)
        self._draw_textures(bp.layers)
        self._create_horizontal_lines(bp.max_depth)
        self._create_title(bp.title)
        description_lines = self._create_descriptions(bp.layers)
        self._create_switch_lines(bp.layers, description_lines)
        self._create_height(bp.height)
        return self.image


if __name__ == "__main__":
    with open("bohrprofil.txt", "r") as file:
        bp = Bohrprofil.unmarshal(eval(file.read()))
    drawer = BohrprofilDrawer()
    img = drawer.draw_profile(bp)
    img.save("bohrprofil.png")
