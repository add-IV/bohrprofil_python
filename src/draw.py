from tkinter import *
from PIL import Image, ImageDraw, ImageFont
from os import path

from PIL import Image, ImageTk

from .bohrprofil import Bohrprofil, Layer
from .config import Config

from .utils import get_pixels_per_cm


def _get_bounds_xy(draw: ImageDraw, font: ImageFont, text: str) -> tuple[int, int]:
    bbox = draw.multiline_textbbox((0, 0), text, font=font)
    return bbox[2] + bbox[0], bbox[3] + bbox[1]


class BohrprofilDrawer:
    basedir = path.dirname(__file__)

    def _create_scale(self, max_depth: float):
        for i in range(int(max_depth) + 1):
            text = f"{i}.00 m"
            y = get_pixels_per_cm(i) + self.config.y1()
            size = self.config.get("Schriften", "Maßstab Schriftgröße")
            font = self.draw.getfont().font_variant(size=size)
            start_x = self.config.x1()
            endx = self.config.x2()
            boundsxy = _get_bounds_xy(self.draw, font, text)
            self.draw.text(
                (
                    endx
                    - boundsxy[0]
                    + self.config.get("Schriften Abstände", "Maßstab X Abstand"),
                    y
                    - boundsxy[1]
                    + self.config.get("Schriften Abstände", "Maßstab Y Abstand"),
                ),
                text,
                fill=self.font_color,
                font=font,
            )
            width = self.config.get("Linien", "Maßstab Linienstärke")
            self.draw.line((start_x, y, endx, y), fill=self.line_color, width=width)

    def _custom_resize(self, img: Image, height: int) -> Image:
        # repeats the image until the height is reached
        img_height = img.height
        img_width = img.width
        new_img = Image.new("1", (img_width, height))
        for y in range(0, height, img_height):
            new_img.paste(img, (0, y))
        return new_img

    def _draw_textures(self, layers: list[Layer]):
        start_y = self.config.y1()
        image_width = self.config.get("Abstände und Längen", "Symbole Länge")
        start_x = self.config.x4()
        for layer in layers:
            y = get_pixels_per_cm(layer.end_depth) + self.config.y1()
            texture = layer.texture
            img = Image.open(
                path.join(self.basedir, "..", "patterns", f"{texture}.png")
            )
            aspect_ratio = img.width / img.height
            img = img.resize((image_width, int(image_width / aspect_ratio)))
            img = self._custom_resize(img, int(y - start_y) + 1)
            self.image.paste(img, (start_x, int(start_y)))
            start_y = y

    def _create_horizontal_lines(self, max_depth: float):
        start_x = self.config.x4()
        end_x = self.config.x5()
        self.draw.rectangle(
            (
                start_x,
                self.config.y1(),
                end_x,
                get_pixels_per_cm(max_depth) + self.config.y1(),
            ),
            outline=self.line_color,
            width=self.config.get("Linien", "Profil Linienstärke"),
        )

    def _create_switch_lines(self, layers: list[Layer], description_lines: list[float]):
        self.draw.line(
            (self.config.x3(), self.config.y1(), self.config.x7(), self.config.y1()),
            fill=self.line_color,
            width=self.config.get("Linien", "Profil Linienstärke"),
        )
        size = self.config.get("Schriften", "Schichtentiefe Schriftgröße")
        font = self.draw.getfont().font_variant(size=size)
        for i in range(len(layers)):
            text = f"{(layers[i].end_depth):.2f} m"
            boundsxy = _get_bounds_xy(self.draw, font, text)
            self.draw.text(
                (
                    self.config.x3()
                    + self.config.get("Schriften Abstände", "Schichtentiefe X Abstand"),
                    get_pixels_per_cm(layers[i].end_depth)
                    + self.config.y1()
                    - boundsxy[1]
                    + self.config.get("Schriften Abstände", "Schichtentiefe Y Abstand"),
                ),
                text,
                font=font,
                fill=self.font_color,
            )
            self.draw.line(
                [
                    self.config.x3(),
                    get_pixels_per_cm(layers[i].end_depth) + self.config.y1(),
                    self.config.x5(),
                    get_pixels_per_cm(layers[i].end_depth) + self.config.y1(),
                    self.config.x6(),
                    description_lines[i],
                    self.config.x7(),
                    description_lines[i],
                ],
                fill=self.line_color,
                width=self.config.get("Linien", "Profil Linienstärke"),
            )

    def _create_title(self, title: str):
        size = self.config.get("Schriften", "Titel Schriftgröße")
        font = self.draw.getfont().font_variant(size=size)
        boundsxy = _get_bounds_xy(self.draw, font, title)
        self.draw.text(
            (
                self.config.get_width() // 2
                - boundsxy[0] // 2
                + self.config.get("Schriften Abstände", "Titel Offset"),
                self.config.get("Schriften Abstände", "Titel Abstand"),
            ),
            title,
            fill=self.font_color,
            font=font,
        )

    def _create_descriptions(self, layers: list[Layer]) -> list[float]:
        description_lines = []
        size = self.config.get("Schriften", "Beschreibung Schriftgröße")
        font = self.draw.getfont().font_variant(size=size)
        current_y = get_pixels_per_cm(1)
        y_border = self.config.get("Schriften Abstände", "Beschreibung Y Abstand")
        for layer in layers:
            current_y += y_border
            boundsxy = _get_bounds_xy(self.draw, font, layer.description)
            self.draw.text(
                (
                    self.config.x6()
                    + self.config.get("Schriften Abstände", "Beschreibung X Abstand"),
                    current_y,
                ),
                layer.description,
                fill=self.font_color,
                font=font,
            )
            current_y += boundsxy[1] + y_border
            if current_y < get_pixels_per_cm(layer.end_depth) + self.config.y1():
                current_y = get_pixels_per_cm(layer.end_depth) + self.config.y1()
            description_lines.append(current_y)
        return description_lines

    def _create_height(self, height: float):
        size = self.config.get("Schriften", "Meereshöhe Schriftgröße")
        font = self.draw.getfont().font_variant(size=size)
        text = f"Meereshöhe: {height} m NN"
        boundsxy = _get_bounds_xy(self.draw, font, text)
        self.draw.text(
            (
                self.config.x3()
                + self.config.get("Schriften Abstände", "Meereshöhe X Abstand"),
                self.config.y1()
                - boundsxy[1]
                + self.config.get("Schriften Abstände", "Meereshöhe Y Abstand"),
            ),
            text,
            fill=self.font_color,
            font=font,
        )

    def _new_image(self, width: int, height: int):
        self.image = Image.new(
            "RGB",
            (width, height),
            color=self.background_color,
        )
        self.draw = ImageDraw.Draw(self.image)
        self.draw.font = ImageFont.truetype(
            path.join(self.basedir, "..", "DejaVuSans.ttf"),
            self.config.get("Schriften", "Schriftgröße"),
        )

    def draw_profile(self, bp: Bohrprofil, config: Config) -> Image:
        self.config = config
        self.background_color = config.get_section("Farben")["Hintergrundfarbe"]
        self.line_color = config.get_section("Farben")["Linienfarbe"]
        self.font_color = config.get_section("Farben")["Schriftfarbe"]
        self._new_image(
            config.get_width(),
            int(get_pixels_per_cm(bp.max_depth) + config.get_extra_height()),
        )
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
