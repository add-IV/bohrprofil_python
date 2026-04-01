# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

A desktop application for creating and visualizing geological borehole profiles (Bohrprofile). Users define soil/rock layers with depth, texture, and description; the app renders a scaled visual profile and exports it as PNG or PDF. The UI is in German.

## Running and building

```bash
# Run the app
python app.py

# Install dependencies
pip install -r requirements.txt

# Build Windows executable
pyinstaller app.spec
```

The PyInstaller spec bundles `mu.ico`, `DejaVuSans.ttf`, `patterns/`, and `config.ini` into the dist folder automatically.

## Architecture

**Data flow:**
1. User edits layers in `LayerList` UI widgets
2. `MainFrame` collects inputs into a `Bohrprofil` object (from `src/bohrprofil.py`)
3. `BohrprofilDrawer` (`src/draw.py`) renders the profile to a PIL `Image` at 300 DPI
4. Image is shown on a scrollable Tkinter canvas or exported as PNG/PDF

**Key modules:**
- `src/bohrprofil.py` — Data model: `Layer` (end_depth, texture, description) and `Bohrprofil` (title, height, max_depth, layers). Handles JSON save/load.
- `src/main_frame.py` — Main UI controller: menu, canvas, file operations, triggers redraw on any change.
- `src/draw.py` — All rendering logic. `BohrprofilDrawer` draws scale, texture tiles, lines, and text onto a PIL image.
- `src/config.py` — Reads `config.ini` and exposes layout constants (spacing, colors, fonts). All dimensions are in cm, converted to pixels via `PIXEL_PER_CM = 118.11` (300 DPI).
- `src/utils.py` — DPI/pixel helpers, path resolution for both dev and frozen (PyInstaller) environments.

**Path handling:** The app uses `utils.get_external_dir()` and `utils.get_bundled_dir()` to find assets. When frozen by PyInstaller, `sys._MEIPASS` points to bundled files; otherwise the project root is used. When writing user-modifiable files (config, patterns), always use `get_external_dir()`.

**Configuration:** `config.ini` controls all visual layout parameters. The `[Abstände und Längen]` section defines spacing/dimensions in cm, `[Farben]` colors, `[Schriften]` font paths and sizes. Changing these affects the rendered output without code changes.

## No test suite

There are no automated tests. Verify changes by running the app and checking the canvas render and export output. `bohrprofil.json` can be used as sample data via File → Open.
