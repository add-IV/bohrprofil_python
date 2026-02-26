# -*- mode: python ; coding: utf-8 -*-
import shutil
import os


a = Analysis(
    ["app.py"],
    pathex=[],
    binaries=[],
    datas=[
        ("mu.ico", "."),
        ("DejaVuSans.ttf", "."),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    exclude_binaries=False,
    name="Bohrprofil",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon="mu.ico",
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

shutil.copytree("patterns", "dist/patterns", dirs_exist_ok=True)
shutil.copy("config.ini", "dist/config.ini")
