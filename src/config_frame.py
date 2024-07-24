from tkinter import *
from tkinter import ttk

from .config import Config


class ConfigFrame(ttk.Frame):
    def __init__(
        self, master, config: Config, updatecallback: callable, resetcallback: callable
    ):
        super().__init__(master)
        self.config = config
        self.update = updatecallback
        self.reset_frame = resetcallback

        self.grid(row=0, column=1, sticky=(N, W, E, S), padx=8, pady=4)

        self.current_row = 0

        for section in [
            "Abstände und Längen",
            "Farben",
            "Schriften",
            "Schriften Abstände",
            "Linien",
        ]:
            self.create_section_title(section)
            self.create_config_section(section, self.config.get_section(section))
            self.create_separator()

        self.reset_button = ttk.Button(self, text="Zurücksetzen", command=self.reset)
        self.reset_button.grid(row=self.current_row, column=0, sticky=(N, W))

        self.save_button = ttk.Button(self, text="Speichern", command=self.save)
        self.save_button.grid(row=self.current_row, column=1, sticky=(N, W))

    def save(self):
        self.config.save()

    def create_section_title(self, title: str):
        label = ttk.Label(self, text=title)
        label.grid(row=self.current_row, column=0, sticky=(N, W))
        self.current_row += 1

    def create_separator(self):
        separator = ttk.Separator(self, orient=HORIZONTAL)
        separator.grid(row=self.current_row, column=0, sticky=(W, E))
        self.current_row += 1

    def create_config_section(self, section: str, options: dict):
        for key, value in options.items():
            self.create_config_option(section, key, value)

    def create_config_option(self, section: str, key: str, value: str):
        label = ttk.Label(self, text=f"{key}:")
        label.grid(row=self.current_row, column=0, sticky=(N, W))

        entry = ttk.Entry(self)
        entry.grid(row=self.current_row, column=1, sticky=(N, W, E))
        entry.insert(0, value)

        self.current_row += 1

        entry.bind("<FocusOut>", lambda e: self.set_value(section, key, entry.get()))

    def set_value(self, section, key, value):
        self.config.set(section, key, value)
        self.update()

    def reset(self):
        self.config.read_default_config()
        self.update()
        self.reset_frame()
