# -*- coding: utf-8 -*-
"""
Build Standalone Single-File Windows Executable: Tsukihime_BYOA_Importer.exe
============================================================================
Uses PyInstaller to package scripts/byoa_gui.py (+ byoa_import, transpile_tsukihime,
build_ui_theme) into a self-contained GUI/CLI executable requiring zero Python install.
"""

import os
import sys
import shutil
import hashlib
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST_DIR = os.path.join(ROOT, "dist")
BUILD_DIR = os.path.join(ROOT, "build_pyinstaller")
ICON_PATH = os.path.join(ROOT, "Tsukihime_HD", "icon.ico")
ENTRY = os.path.join(ROOT, "scripts", "byoa_gui.py")
EXE_NAME = "BYOA_Importer"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    os.makedirs(DIST_DIR, exist_ok=True)
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--clean",
        "--onefile",
        "--windowed",
        "--name", EXE_NAME,
        "--distpath", DIST_DIR,
        "--workpath", BUILD_DIR,
        "--specpath", BUILD_DIR,
        "--paths", os.path.join(ROOT, "scripts"),
        "--hidden-import", "byoa_import",
        "--hidden-import", "transpile_tsukihime",
        "--hidden-import", "build_ui_theme",
    ]
    if os.path.isfile(ICON_PATH):
        sep = ";" if sys.platform == "win32" else ":"
        cmd.extend(["--icon", ICON_PATH, "--add-data", f"{ICON_PATH}{sep}."])

    # Strip unrelated heavy libraries to keep the standalone .exe lean
    for ex_mod in (
        "matplotlib", "scipy", "pandas", "IPython", "jupyter", "notebook",
        "pytest", "PyQt5", "PyQt6", "PySide2", "PySide6", "wx",
        "torch", "tensorflow", "cv2", "sklearn", "sympy", "h5py",
    ):
        cmd.extend(["--exclude-module", ex_mod])

    cmd.append(ENTRY)
    print("Running:", " ".join(cmd))
    res = subprocess.run(cmd, encoding="utf-8", errors="replace")
    if res.returncode != 0:
        sys.exit(res.returncode)

    exe_path = os.path.join(DIST_DIR, EXE_NAME + (".exe" if sys.platform == "win32" else ""))
    if not os.path.isfile(exe_path):
        print(f"[ERROR] Expected executable not found: {exe_path}")
        sys.exit(1)

    # Copy built exe cleanly into project root for immediate local use & write SHA256
    root_exe = os.path.join(ROOT, os.path.basename(exe_path))
    shutil.copy2(exe_path, root_exe)
    digest = sha256_file(root_exe)
    sz_mb = os.path.getsize(root_exe) / (1024 * 1024)
    print(f"\n[OK] Built standalone BYOA Importer: {root_exe} ({sz_mb:.2f} MB)")
    print(f"     SHA-256: {digest}")

    # Clean intermediate build directories so workspace stays spotless
    shutil.rmtree(BUILD_DIR, ignore_errors=True)
    shutil.rmtree(DIST_DIR, ignore_errors=True)


if __name__ == "__main__":
    main()
