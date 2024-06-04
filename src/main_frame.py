from tkinter import *
from tkinter import ttk

from layer_list import LayerList

from draw import draw_profile
from bohrprofil import Bohrprofil, Layer
from src.utils import get_pixels_per_cm


class MainFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=0, sticky=(N, W, E, S), padx=8, pady=4)

        self.info_frame = ttk.Frame(self)
        self.info_frame.grid(row=0, column=0, sticky=(N, W))

        self.title_label = ttk.Label(self.info_frame, text="Title:")
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
            self.layer_manipulation_frame, text="Add Layer"
        )
        self.add_layer_button.grid(row=0, column=0, sticky=(N, W))

        self.remove_layer_button = ttk.Button(
            self.layer_manipulation_frame, text="Remove Layer"
        )
        self.remove_layer_button.grid(row=0, column=1, sticky=(N, W))

        self.sort_layers_button = ttk.Button(
            self.layer_manipulation_frame, text="Sort Layers"
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

        self.save_button = ttk.Button(self, text="Save")
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
        bohrprofil = Bohrprofil(self.title_name.get(), self.height_name.get(), 100, layers)
        bohrprofil.sort_layers()
        bohrprofil.update_max_depth()
        draw_profile(self.canvas, bohrprofil, self.canvas_frame.winfo_height())

    def save(self):
        pass
