from tkinter import *
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename

from PIL import ImageTk

from .layer_list import LayerList

from .draw import BohrprofilDrawer
from .bohrprofil import Bohrprofil, Layer
from .utils import get_pixels_per_cm
from .config_frame import ConfigFrame
from .config import Config


class MainFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.drawer = BohrprofilDrawer()
        self.config = Config()

        self.grid(row=0, column=0, sticky=(N, W, E, S), padx=8, pady=4)

        self.info_frame = ttk.Frame(self)
        self.info_frame.grid(row=0, column=0, sticky=(N, W))

        self.title_label = ttk.Label(self.info_frame, text="Titel:")
        self.title_label.grid(row=0, column=0, sticky=(N, W))

        self.title_name = StringVar()
        self.title_entry = ttk.Entry(self.info_frame, textvariable=self.title_name)
        self.title_entry.grid(row=1, column=0, sticky=(N, W))
        self.title_name.set("Bohrprofil")

        self.height_label = ttk.Label(self.info_frame, text="Höhe:")
        self.height_label.grid(row=0, column=1, sticky=(N, W))

        self.height_name = StringVar()
        self.height_entry = ttk.Entry(self.info_frame, textvariable=self.height_name)
        self.height_entry.grid(row=1, column=1, sticky=(N, W))
        self.height_name.set("375")

        self.layer_manipulation_frame = ttk.Frame(self)
        self.layer_manipulation_frame.grid(row=1, column=0, sticky=(N, W))

        self.add_layer_button = ttk.Button(
            self.layer_manipulation_frame, text="Schicht hinzufügen"
        )
        self.add_layer_button.grid(row=0, column=0, sticky=(N, W))

        self.remove_layer_button = ttk.Button(
            self.layer_manipulation_frame, text="Schicht entfernen"
        )
        self.remove_layer_button.grid(row=0, column=1, sticky=(N, W))

        self.sort_layers_button = ttk.Button(
            self.layer_manipulation_frame, text="Schichten sortieren"
        )
        self.sort_layers_button.grid(row=0, column=2, sticky=(N, W))

        self.layer_list = LayerList(self, self.update)
        self.layer_list.grid(row=2, column=0, sticky=(N, W, E, S))

        self.canvas_frame = ttk.Frame(self)
        self.canvas_frame.grid(row=0, column=2, rowspan=3, sticky=(N, W, S))

        self.canvas = Canvas(
            self.canvas_frame,
            width=get_pixels_per_cm(7),
            height=get_pixels_per_cm(2),
            background="white",
        )
        self.canvas.grid(row=0, column=0, sticky=(N, W))

        self.scrollbar = ttk.Scrollbar(
            self.canvas_frame, orient=VERTICAL, command=self.canvas.yview
        )
        self.scrollbar.grid(row=0, column=2, sticky=(N, S))
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        self.save_button = ttk.Button(self, text="Speichern")
        self.save_button.grid(row=3, column=2, sticky=(N, E))

        self.rowconfigure(2, weight=1)
        self.columnconfigure(1, weight=1)

        self.add_layer_button["command"] = self.layer_list.add_one_layer
        self.remove_layer_button["command"] = self.layer_list.remove_one_layer
        self.sort_layers_button["command"] = self.layer_list.sort_layers
        self.save_button["command"] = self.save
        self.title_entry.bind("<KeyRelease>", self.update)
        self.height_entry.bind("<KeyRelease>", self.update)

        self.after(100, self.update)
        self.after(100, self.open_config_toplevel)

    def update(self, event=None):
        layers = []
        for layer in self.layer_list.layers:
            layers.append(
                Layer(
                    float(layer.end_depth.get().replace(",", ".")),
                    layer.texture.get(),
                    layer.description_text.get(1.0, END),
                )
            )
        self.bohrprofil = Bohrprofil(
            self.title_name.get(), self.height_name.get(), 100, layers
        )
        self.bohrprofil.sort_layers()
        self.bohrprofil.update_max_depth()
        self.canvas.delete("all")
        self.canvas.config(
            width=self.config.get_width(),
            height=self.canvas_frame.winfo_height(),
            background="white",
            scrollregion=(
                0,
                0,
                self.config.get_width(),
                int(get_pixels_per_cm(self.bohrprofil.max_depth))
                + self.config.get_extra_height(),
            ),
        )
        self.image = self.drawer.draw_profile(self.bohrprofil, self.config)
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor=NW, image=self.photo)

    def update_config(self):
        self.config = self.config_frame.config
        self.update()

    def save(self):
        filename = asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*")],
        )
        if filename:
            self.image.save(filename)

    def open_config_toplevel(self):
        self.config_toplevel = Toplevel(self)
        self.config_toplevel.title("Config")
        self.config_toplevel.minsize(200, 600)
        self.config_toplevel.resizable(False, False)
        self.config_toplevel.columnconfigure(0, weight=1)
        self.config_toplevel.rowconfigure(0, weight=1)
        self.config_frame = ConfigFrame(
            self.config_toplevel, self.config, self.update_config
        )
        self.config_toplevel.transient(self)
        self.config_toplevel.wait_window(self.config_toplevel)
