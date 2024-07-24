from configparser import ConfigParser
import os

from .utils import get_pixels_per_cm


class Config:
    def __init__(self):
        self.parser = ConfigParser()
        self.read_default_config()

    def get(self, section, key):
        value = self.parser.get(section, key)
        if value.endswith("cm"):
            return int(get_pixels_per_cm(int(value[:-2])))
        if value[0] in ("-", "+") and value[1:].isdigit() or value.isdigit():
            return int(value)
        return value

    def get_section(self, section):
        return self.parser[section]

    def set(self, section, key, value):
        print(f"Setting {section}: {key} to {value}")
        if not self.parser.has_section(section):
            self.parser.add_section(section)
        self.parser.set(section, key, value)

    def get_extra_height(self):
        return self.get("Abstände und Längen", "Erste Ebene Abstand") + self.get(
            "Abstände und Längen", "Letzte Ebene Abstand"
        )

    def get_width(self):
        return (
            self.get("Abstände und Längen", "Links Abstand")
            + self.get("Abstände und Längen", "Maßstab Länge")
            + self.get("Abstände und Längen", "Mitte Abstand")
            + self.get("Abstände und Längen", "Schichtentiefe Länge")
            + self.get("Abstände und Längen", "Symbole Länge")
            + self.get("Abstände und Längen", "Beschreibung Abstand")
            + self.get("Abstände und Längen", "Beschreibung Länge")
            + self.get("Abstände und Längen", "Rechts Abstand")
        )

    def read_file(self, filename):
        self.parser.read(filename, encoding="utf-8")

    def write_file(self, filename):
        with open(filename, "w", encoding="utf-8") as file:
            self.parser.write(file)

    def read_default_config(self):
        self.parser.read_string(
            """
            [Abstände und Längen]
            Erste Ebene Abstand = 1cm
            Letzte Ebene Abstand = 1cm
            Links Abstand = 80
            Maßstab Länge = 160
            Mitte Abstand = 80
            Schichtentiefe Länge = 80
            Symbole Länge = 64
            Beschreibung Abstand = 40
            Beschreibung Länge = 200
            Rechts Abstand = 80

            [Farben]
            Hintergrundfarbe = white
            Linienfarbe = black
            Schriftfarbe = black

            [Schriften]
            Schriftart = DejaVuSans.ttf
            Schriftgröße = 15
            Maßstab Schriftgröße = 25
            Schichtentiefe Schriftgröße = 15
            Titel Schriftgröße = 35
            Beschreibung Schriftgröße = 15
            Meereshöhe Schriftgröße = 12

            [Schriften Abstände]
            Titel offset = 0
            Titel Abstand = 10
            Maßstab X Abstand = -5
            Maßstab Y Abstand = 0
            Schichtentiefe X Abstand = +5
            Schichtentiefe Y Abstand = 0
            Beschreibung X Abstand = 0
            Beschreibung Y Abstand = 0
            Meereshöhe X Abstand = 5
            Meereshöhe Y Abstand = -5
            
            [Linien]
            Maßstab Linienstärke = 3
            Profil Linienstärke = 1
            """
        )


config = Config()
dict = config.parser._sections
