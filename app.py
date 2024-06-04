from tkinter import *
from tkinter import ttk
from os import path
from src.main_frame import MainFrame
from src.utils import get_pixels_per_cm

basedir = path.dirname(__file__)

layers = []

root = Tk()
root.title("Bohrprofil")
root.minsize(1400, 800)
root.geometry("1400x800")

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Create a main frame
main_frame = MainFrame(root)

root.iconbitmap(path.join(basedir, "mu.ico"))

root.mainloop()
