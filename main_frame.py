from tkinter import *
from tkinter import ttk

from layer_list import LayerList

from draw import draw_profile
from bohrprofil import Bohrprofil, Layer
from utils import get_pixels_per_cm

class MainFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=0, sticky=(N, W, E, S), padx=8, pady=4)

        self.title_label = ttk.Label(self, text="Title:")
        self.title_label.grid(row=0, column=0, sticky=(N, W))

        self.title_entry = ttk.Entry(self)
        self.title_entry.grid(row=1, column=0, sticky=(N, W))

        self.layer_manipulation_frame = ttk.Frame(self)
        self.layer_manipulation_frame.grid(row=2, column=0, sticky=(N, W))

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
        self.layer_list.grid(row=3, column=0, rowspan=2, sticky=(N, W, E, S))

        self.canvas_frame = ttk.Frame(self)
        self.canvas_frame.grid(row=0, column=2, rowspan=4, sticky=(N, W))
        

        self.canvas = Canvas(self.canvas_frame, width=get_pixels_per_cm(7), height=get_pixels_per_cm(2), background="white")
        self.canvas.grid(row=0, column=0, sticky=(N, W))

        # self.scrollbar = ttk.Scrollbar(self.canvas_frame, orient=VERTICAL, command=self.canvas.yview)
        # self.scrollbar.grid(row=0, column=2, sticky=(N, S))

        self.save_button = ttk.Button(self, text="Save")
        self.save_button.grid(row=4, column=2, sticky=(N, E))

        self.rowconfigure(3, weight=1)
        self.columnconfigure(1, weight=1)

        self.add_layer_button["command"] = self.layer_list.add_one_layer
        self.remove_layer_button["command"] = self.layer_list.remove_one_layer
        self.sort_layers_button["command"] = self.layer_list.sort_layers

    def update(self, event=None):
        layers = []
        for layer in self.layer_list.layers:
            layers.append(Layer(float(layer.end_depth.get()), layer.texture.get(), layer.description_text.get(1.0, END)))
        bohrprofil = Bohrprofil(self.title_entry.get(), 100, 100, layers)
        bohrprofil.sort_layers()
        bohrprofil.update_max_depth()
        draw_profile(self.canvas, bohrprofil)