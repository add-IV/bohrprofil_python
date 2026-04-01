from tkinter import Toplevel, Label
from PIL import Image, ImageTk
from os import path

# 2×3 tiles of the standard 104×48 pattern images
_PREVIEW_W = 104
_PREVIEW_H = 96


class TextureHoverPreview:
    """Floating texture preview that appears next to the mouse when hovering
    over options in a ttk.Combobox dropdown.

    Usage:
        preview = TextureHoverPreview(combobox, patterns_dir)
    """

    def __init__(self, combobox, patterns_dir: str):
        """
        combobox:     ttk.Combobox to attach to
        patterns_dir: path to the directory containing <texture>.png files
        """
        self._combobox = combobox
        self._patterns_dir = patterns_dir
        self._tooltip = None
        self._label = None
        self._cache: dict[str, ImageTk.PhotoImage] = {}
        self._listbox_bound = False
        self._listbox_path = None

        combobox.bind("<ButtonPress-1>", self._on_open, add="+")

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _on_open(self, event):
        # The popdown window is created after the click is processed.
        self._combobox.after(50, self._bind_listbox)

    def _bind_listbox(self):
        if self._listbox_bound:
            return
        try:
            popdown = self._combobox.tk.eval(
                f"ttk::combobox::PopdownWindow {self._combobox}"
            )
            if not popdown:
                return
            listbox_path = popdown + ".f.l"

            # The listbox is a pure Tcl/Tk widget with no Python wrapper,
            # so nametowidget() won't find it — bind via Tcl directly.
            motion_cmd = self._combobox.register(self._on_motion_tcl)
            leave_cmd = self._combobox.register(self._on_leave_tcl)
            self._combobox.tk.eval(f"bind {listbox_path} <Motion> {{{motion_cmd} %x %y}}")
            self._combobox.tk.eval(f"bind {listbox_path} <Leave> {{{leave_cmd}}}")
            self._combobox.tk.eval(f"bind {listbox_path} <Unmap> {{{leave_cmd}}}")

            self._listbox_path = listbox_path
            self._listbox_bound = True
        except Exception:
            return

    def _on_motion_tcl(self, x, y):
        x, y = int(x), int(y)
        try:
            index = int(self._combobox.tk.call(self._listbox_path, "nearest", y))
        except Exception:
            self._hide()
            return
        values = self._combobox["values"]
        if not values or index < 0 or index >= len(values):
            self._hide()
            return
        img = self._load(values[index])
        if img is None:
            self._hide()
            return
        root_x = int(self._combobox.tk.call("winfo", "rootx", self._listbox_path))
        root_y = int(self._combobox.tk.call("winfo", "rooty", self._listbox_path))
        self._show(img, root_x + x + 16, root_y + y + 8)

    def _on_leave_tcl(self):
        self._hide()

    def _show(self, img: ImageTk.PhotoImage, x: int, y: int):
        if self._tooltip is None:
            self._tooltip = Toplevel(self._combobox)
            self._tooltip.overrideredirect(True)
            self._tooltip.attributes("-topmost", True)
            self._label = Label(self._tooltip, borderwidth=1, relief="solid")
            self._label.pack()
        self._label.configure(image=img)
        self._label.image = img  # prevent GC
        self._tooltip.geometry(f"+{x}+{y}")
        self._tooltip.deiconify()

    def _hide(self):
        if self._tooltip is not None:
            self._tooltip.withdraw()

    def _load(self, texture_name: str) -> ImageTk.PhotoImage | None:
        if texture_name in self._cache:
            return self._cache[texture_name]
        img_path = path.join(self._patterns_dir, f"{texture_name}.png")
        if not path.exists(img_path):
            return None
        try:
            src = Image.open(img_path)
            # Tile the pattern to fill the preview area.
            preview = Image.new(src.mode, (_PREVIEW_W, _PREVIEW_H))
            for tile_y in range(0, _PREVIEW_H, src.height):
                for tile_x in range(0, _PREVIEW_W, src.width):
                    preview.paste(src, (tile_x, tile_y))
            tk_img = ImageTk.PhotoImage(preview)
            self._cache[texture_name] = tk_img
            return tk_img
        except Exception:
            return None
