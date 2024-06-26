from tkinter import *
from tkinter import ttk

from .layer import Layer
from .vertical_scrolled_frame import VerticalScrolledFrame


class LayerList(VerticalScrolledFrame):
    def __init__(self, parent, change_callback=None):
        super().__init__(parent)
        self.layers = []
        self.change_callback = change_callback

        self.end_depth_label = ttk.Label(self.interior, text="End depth")
        self.end_depth_label.grid(row=0, column=0, sticky=(N, W))

        self.texture_label = ttk.Label(self.interior, text="Texture")
        self.texture_label.grid(row=0, column=1, sticky=(N, W))

        self.description_label = ttk.Label(self.interior, text="Description")
        self.description_label.grid(row=0, column=2, sticky=(N, W))

        self.add_one_layer(False)

    def add_one_layer(self, do_callback=True):
        layer = Layer(self.interior, len(self.layers) + 1, self.change_callback)
        self.layers.append(layer)
        layer.set_all(f"{len(self.layers)}", "")
        if do_callback:
            self.change_callback()

    def remove_one_layer(self):
        if len(self.layers) > 1:
            layer = self.layers.pop()
            layer.forget()
            del layer
            self.change_callback()

    def sort_layers(self):
        self.layers.sort(key=lambda x: x.end_depth.get())
        for i, layer in enumerate(self.layers):
            layer.end_depth_entry.grid(row=i + 1, column=0, sticky=(N, W))
            layer.texture_combobox.grid(row=i + 1, column=1, sticky=(N, W))
            layer.description_text.grid(row=i + 1, column=2, sticky=(N, W))
        self.change_callback()
