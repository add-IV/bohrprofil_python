from tkinter import *
from tkinter import ttk

from src.utils import get_textures


class Layer:
    def __init__(self, master, rownumber, change_callback=None):

        self.end_depth = StringVar()
        self.end_depth_entry = ttk.Entry(
            master,
            textvariable=self.end_depth,
            width=10,
            validate="focusout",
            validatecommand=change_callback,
        )
        self.end_depth_entry.grid(row=rownumber, column=0, sticky=(N, W))

        self.texture = StringVar()
        self.texture_combobox = ttk.Combobox(master, textvariable=self.texture)
        self.texture_combobox.grid(row=rownumber, column=1, sticky=(N, W))
        self.texture_combobox.bind("<<ComboboxSelected>>", change_callback)
        self.combobox_set_textures()

        self.description_text = Text(master, width=38, height=4)
        self.description_text.grid(row=rownumber, column=2, sticky=(N, W))
        self.description_text.bind("<KeyRelease>", change_callback)

    def set_all(self, end_depth, description):
        self.end_depth.set(end_depth)
        self.description_text.delete(1.0, END)
        self.description_text.insert(1.0, description)

    def forget(self):
        self.end_depth_entry.grid_forget()
        self.texture_combobox.grid_forget()
        self.description_text.grid_forget()

    def combobox_set_textures(self):
        self.texture_combobox["values"] = get_textures()
        if len(self.texture_combobox["values"]) > 0:
            self.texture_combobox.current(0)
