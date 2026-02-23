from tkinter import *
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter import messagebox

import sys
import os
import subprocess

if sys.platform == "win32":
    import win32api
from PIL import ImageTk, Image

import tempfile
import io


from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader

from .layer_list import LayerList

from .draw import BohrprofilDrawer
from .bohrprofil import Bohrprofil, Layer
from .utils import get_pixels_per_cm, open_textures_dir
from .config_frame import ConfigFrame
from .config import Config


class MainFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.create_menubar(master)
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

        self.add_layer_button = ttk.Button(
            self.info_frame, text="Schicht hinzufügen"
        )
        self.add_layer_button.grid(row=2, column=0, sticky=(N, W))

        self.remove_layer_button = ttk.Button(
            self.info_frame, text="Schicht entfernen"
        )
        self.remove_layer_button.grid(row=2, column=1, sticky=(N, W))

        self.layer_list = LayerList(self, self.update)
        self.layer_list.grid(row=2, column=0, sticky=(N, W, E, S))
        self.layer_list.add_one_layer(False)

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

        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

        self.add_layer_button["command"] = self.layer_list.add_one_layer
        self.remove_layer_button["command"] = self.layer_list.remove_one_layer
        self.title_entry.bind("<KeyRelease>", self.update)
        self.height_entry.bind("<KeyRelease>", self.update)

        self.after(100, self.update)

    def update(self, event=None):
        self.layer_list.sort_layers()
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
        self.layer_list.set_max_depth(self.bohrprofil.max_depth)
        self.canvas.delete("all")
        height = (
            int(get_pixels_per_cm(self.bohrprofil.max_depth))
            + self.config.get_extra_height()
        )
        self.canvas.config(
            width=self.config.get_width(),
            height=min(self.canvas_frame.winfo_height(), height),
            background="white",
            scrollregion=(
                0,
                0,
                self.config.get_width(),
                height,
            ),
        )
        self.image = self.drawer.draw_profile(self.bohrprofil, self.config)
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor=NW, image=self.photo)

    def update_config(self):
        self.config = self.config_frame.config
        self.update()

    def save(self, filename):
        if not filename.endswith(".pdf"):
            self.image.save(filename)
        else:
            image_data = io.BytesIO()
            self.image.save(image_data, format="png")
            image_data.seek(0)

            # create a A4 pdf with reportlab

            image_height = self.image.height
            image_width = self.image.width
            scale = 300.0
            image_height = image_height * 72 / scale
            image_width = image_width * 72 / scale

            c = canvas.Canvas(filename, pagesize=A4)
            image_out = ImageReader(image_data)
            c.drawImage(image_out, 40, A4[1] - image_height - 40, width=image_width, height=image_height)
            c.showPage()
            c.save()


    def create_menubar(self, root):
        menubar = Menu(root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Neu", command=self._new)
        filemenu.add_command(label="Öffnen", command=self._open)
        filemenu.add_command(label="Speichern", command=self._save)
        filemenu.add_separator()
        filemenu.add_command(label="Exportieren", command=self._export)
        filemenu.add_command(label="Drucken", command=self._print)
        filemenu.add_separator()
        filemenu.add_command(label="Beenden", command=root.quit)
        optionmenu = Menu(menubar, tearoff=0)
        optionmenu.add_command(label="Konfigurieren", command=self._config)
        optionmenu.add_command(label="Öffne Symbolverzeichnis", command=self._open_symbol_dir)
        menubar.add_cascade(label="Datei", menu=filemenu)
        menubar.add_cascade(label="Optionen", menu=optionmenu)
        root.config(menu=menubar)

    def _open_symbol_dir(self):
        open_textures_dir()

    def _new(self):
        self.title_name.set("Bohrprofil")
        self.height_name.set("375")
        self.layer_list.clear()
        self.update()

    def _open(self):
        filename = askopenfilename(
            filetypes=[("Json files", "*.json"), ("All files", "*")]
        )
        if filename == "":
            return
        bohrprofil = Bohrprofil.load(filename)
        self.title_name.set(bohrprofil.title)
        self.height_name.set(bohrprofil.height)
        self.layer_list.clear()
        first_layer_info = bohrprofil.layers[0]
        self.layer_list.layers[0].set_all(str(first_layer_info.end_depth), first_layer_info.description)
        self.layer_list.layers[0].texture.set(first_layer_info.texture)
        for layer in bohrprofil.layers[1:]:
            self.layer_list.add_one_layer(False)
            self.layer_list.layers[-1].set_all(str(layer.end_depth), layer.description)
            self.layer_list.layers[-1].texture.set(layer.texture)
        self.update()

    def _save(self):
        filename = asksaveasfilename(
            defaultextension=".json",
            filetypes=[("Json files", "*.json"), ("All files", "*")],
        )
        if filename == "":
            return
        self.bohrprofil.save(filename)


    def _export(self):
        filename = asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Pdf files", "*.pdf"), ("PNG files", "*.png"), ("All files", "*")],
        )
        if filename == "":
            return
        self.save(filename)

    def _print(self):
        filename = tempfile.mktemp(".pdf")
        if filename == "":
            return
        self.save(filename)

        if sys.platform == "win32":
            try:
                win32api.ShellExecute(0, "print", filename, None, ".", 0)
            except Exception as e1:
                try:
                    os.startfile(filename, "print")
                except Exception as e2:
                    try:
                        os.startfile(filename)
                    except Exception as e3:
                        errorinfo = f"win32api:\n{e1}\nos.startfile(print):\n{e2}\nos.startfile:\n{e3}"
                        messagebox.showerror("Drucken fehlgeschlagen", errorinfo)
        elif sys.platform == "linux":
            try:
                subprocess.run(["xdg-open", filename], check=True)
            except Exception as e:
                messagebox.showerror("Drucken fehlgeschlagen", f"Fehler beim Öffnen der Datei:\n{e}")

    def _config(self):
        self.open_config_toplevel()

    def open_config_toplevel(self):
        if hasattr(self, "config_toplevel"):
            self.config_toplevel.destroy()
        self.config_toplevel = Toplevel(self)
        self.config_toplevel.title("Config")
        self.config_toplevel.minsize(200, 600)
        self.config_toplevel.resizable(False, False)
        self.config_toplevel.columnconfigure(0, weight=1)
        self.config_toplevel.rowconfigure(0, weight=1)
        self.config_frame = ConfigFrame(
            self.config_toplevel, self.config, self.update_config, self.reset_config
        )
        self.config_toplevel.transient(self)
        self.config_toplevel.wait_window(self.config_toplevel)

    def reset_config(self):
        self.open_config_toplevel()
