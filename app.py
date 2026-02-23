from tkinter import *
from tkinter import ttk
from os import path
import sys
from src.main_frame import MainFrame
from src.utils import get_pixels_per_cm

if sys.platform == "win32":
    from ctypes import windll

    myappid = "addiv.bohrprofil.1.0"
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


basedir = path.dirname(__file__)

layers = []

root = Tk()
root.title("Bohrprofil")
root.minsize(1600, 800)
root.geometry("1600x800")

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Create a main frame
main_frame = MainFrame(root)

if sys.platform == "win32":
    root.iconbitmap(path.join(basedir, "mu.ico"))

root.mainloop()
