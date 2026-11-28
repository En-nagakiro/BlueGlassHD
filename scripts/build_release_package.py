# -*- coding: utf-8 -*-
"""
Build Flat Zero-Asset Player BYOA Distribution Package (Windows)
================================================================
Produces a flat, ready-to-unzip player release directory & ZIP under release/:
  release/BlueGlassHD-2.0.0-win/
    ├── BlueGlassHD.exe          (Ren'Py 8.5.3 runtime executable, custom Blue Glass Moon icon)
    ├── BYOA_Importer.exe        (Standalone zero-Python GUI importer, auto-detects sibling game/)
    ├── game/                    (100% open-source engine + UI + OFL/IPA fonts, ZERO copyrighted assets)
    ├── lib/ & renpy/
    ├── LICENSE
    ├── THIRD_PARTY_LICENSES.md
    └── 使用说明.txt
"""

import os
import sys
import shutil
import zipfile
import hashlib
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJ = os.path.join(ROOT, "Tsukihime_HD")
RENPY_PY = os.path.join(ROOT, "tools", "renpy_sdk", "renpy-8.5.3-sdk", "lib", "py3-windows-x86_64", "python.exe")
RENPY_SCRIPT = os.path.join(ROOT, "tools", "renpy_sdk", "renpy-8.5.3-sdk", "renpy.py")
LAUNCHER_DIR = os.path.join(ROOT, "tools", "renpy_sdk", "renpy-8.5.3-sdk", "launcher")
RELEASE_DIR = os.path.join(ROOT, "release")
IMPORTER_EXE = os.path.join(ROOT, "BYOA_Importer.exe")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_zero_copyright_leaks(pkg_root):
    """Hard assertion: zero copyrighted original or derived assets inside player release."""
    forbidden_rel = [
        "game/images",
        "game/story",
        "game/saves",
        "game/gui/portraits",
        "game/gui/main_menu.webp",
        "game/gui/title_eclipse_moon.png",
        "game/gui/title_eclipse_kanji.png",
        "game/core/story_variables.rpy",
        "game/core/image_definitions.rpy",
        "game/core/byoa_meta.rpy",
    ]
    leaks = []
    for rel in forbidden_rel:
        if os.path.exists(os.path.join(pkg_root, rel)):
            leaks.append(rel)
    audio_dir = os.path.join(pkg_root, "game", "audio")
    if os.path.isdir(audio_dir):
        for fn in os.listdir(audio_dir):
            if not fn.lower().startswith("ui_"):
                leaks.append(f"game/audio/{fn}")
    if leaks:
        raise RuntimeError(f"BYOA COMPLIANCE FAILURE - copyrighted/derived files leaked into release: {leaks}")
    print("[OK] Release compliance audit passed: ZERO original or derived copyrighted files inside package.")


def main():
    # 1. Verify open-source repo compliance & version sync (options.rpy / byoa_gui.py / READMEs) first
    r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "verify_project.py"), "--compliance-audit"], encoding="utf-8", errors="replace")
    if r.returncode != 0:
        sys.exit(r.returncode)

    # 2. Ensure BYOA_Importer.exe is freshly built
    if not os.path.isfile(IMPORTER_EXE):
        r2 = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "build_importer_exe.py")], encoding="utf-8", errors="replace")
        if r2.returncode != 0:
            sys.exit(r2.returncode)

    # 3. Clean only previous BlueGlassHD build outputs inside release/ (NEVER wipe unrelated user folders!)
    os.makedirs(RELEASE_DIR, exist_ok=True)
    for entry in os.listdir(RELEASE_DIR):
        if entry.startswith(("BlueGlassHD-", "Tsukihime_HD-")):
            full_entry = os.path.join(RELEASE_DIR, entry)
            if os.path.isdir(full_entry):
                shutil.rmtree(full_entry, ignore_errors=True)
            else:
                try:
                    os.remove(full_entry)
                except OSError:
                    pass

    print("[1/3] Running official Ren'Py 8.5.3 Windows distribution builder...")
    cmd = [
        RENPY_PY, RENPY_SCRIPT, LAUNCHER_DIR,
        "distribute", PROJ,
        "--destination", RELEASE_DIR,
        "--package", "win",
        "--no-update",
    ]
    res = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace")
    if res.stdout:
        print(res.stdout.strip())
    if res.returncode != 0:
        print(res.stderr)
        sys.exit(res.returncode)

    # Locate generated Ren'Py win zip
    zips = [f for f in os.listdir(RELEASE_DIR) if f.endswith("-win.zip")]
    if not zips:
        raise FileNotFoundError(f"Expected *-win.zip in {RELEASE_DIR}, found: {os.listdir(RELEASE_DIR)}")
    raw_zip = os.path.join(RELEASE_DIR, zips[0])
    pkg_name = zips[0][:-4]  # e.g. BlueGlassHD-2.0.0-win
    pkg_dir = os.path.join(RELEASE_DIR, pkg_name)

    print(f"[2/3] Assembling flat BYOA player folder: {pkg_dir} ...")
    with zipfile.ZipFile(raw_zip, "r") as zf:
        zf.extractall(RELEASE_DIR)
    os.remove(raw_zip)

    # Drop BYOA_Importer.exe, licenses, and concise Chinese usage guide directly into flat root!
    shutil.copy2(IMPORTER_EXE, os.path.join(pkg_dir, "BYOA_Importer.exe"))
    for doc in ("LICENSE", "THIRD_PARTY_LICENSES.md"):
        shutil.copy2(os.path.join(ROOT, doc), os.path.join(pkg_dir, doc))

    guide_txt = (
        "月姬 Classic HD（Blue Glass Engine BYOA 发行版）使用说明\n"
        "========================================================\n\n"
        "本发行包为非官方开源兼容引擎，不包含任何 TYPE-MOON 原版图像、音频或剧本。\n\n"
        "使用步骤（免装 Python / Ren'Py）：\n"
        "1. 准备好本地合法持有的《月姬 (2000)》原版目录（支持日文原盘 / 月箱 / 汉化版 / 英化版）。\n"
        "2. 双击本目录下的 BYOA_Importer.exe（若 Windows 弹出 SmartScreen 提示，点「更多信息 → 仍要运行」）。\n"
        "3. 点击「浏览...」选中原版目录，确认检测通过后点击右下角「开始导入」（极速模式约 10 秒）。\n"
        "4. 导入完成后点击「启动游戏」（或直接双击 BlueGlassHD.exe），默认全屏启动（F / Alt+Enter 可切换窗口）。\n"
        "5. 游戏界面与导入器均支持中文 / English 实时切换。\n\n"
        "官方发布与反馈（永久免费开源，谨防付费倒卖与过期搬运）：\n"
        "- GitHub 仓库：https://github.com/En-nagakiro/BlueGlassHD\n"
        "- 作者 B 站主页：https://space.bilibili.com/1601243445\n\n"
        "--------------------------------------------------------\n"
        "Tsukihime Classic HD (Blue Glass Engine BYOA Release)\n"
        "--------------------------------------------------------\n\n"
        "Unofficial open-source compatibility engine. Contains NO copyrighted TYPE-MOON art, audio, or scripts.\n\n"
        "Quick Start (No Python or Ren'Py required):\n"
        "1. Locate your legally owned Tsukihime (2000) directory (JP / Tsukibako / CN / EN editions supported).\n"
        "2. Run BYOA_Importer.exe in this folder (if SmartScreen appears, click 'More info -> Run anyway').\n"
        "3. Click 'Browse...' to select your Tsukihime folder, then click 'Start Import' (~10s in Fast Mode).\n"
        "4. Click 'Launch Game' (or run BlueGlassHD.exe). Launches fullscreen by default (F / Alt+Enter toggles).\n"
        "5. Both the importer and in-game UI support live Chinese / English switching.\n\n"
        "Official Links (Free & open-source forever; beware of paid resellers):\n"
        "- GitHub : https://github.com/En-nagakiro/BlueGlassHD\n"
        "- Author : https://space.bilibili.com/1601243445\n\n"
        "Open-source licenses: LICENSE, THIRD_PARTY_LICENSES.md, and game/fonts/LICENSES.txt.\n"
    )
    with open(os.path.join(pkg_dir, "README_使用说明.txt"), "w", encoding="utf-8-sig", newline="\r\n") as gf:
        gf.write(guide_txt)

    # Hard compliance assertion on final unzipped folder!
    verify_zero_copyright_leaks(pkg_dir)

    # Repack clean flat BYOA distribution ZIP (max deflate level=9 to stay comfortably under 100 MB) + SHA-256
    final_zip = os.path.join(RELEASE_DIR, f"{pkg_name}-BYOA.zip")
    print(f"[3/3] Packing distributable archive: {final_zip} ...")
    with zipfile.ZipFile(final_zip, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zout:
        for r_dir, _, fnames in os.walk(pkg_dir):
            for fn in fnames:
                full = os.path.join(r_dir, fn)
                arc = os.path.relpath(full, RELEASE_DIR)
                zout.write(full, arc)

    digest = sha256_file(final_zip)
    with open(final_zip + ".sha256", "w", encoding="ascii") as sf:
        sf.write(f"{digest}  {os.path.basename(final_zip)}\n")

    zip_mb = os.path.getsize(final_zip) / (1024 * 1024)
    print(f"\n[DONE] Player BYOA Release Ready!")
    print(f"  Flat folder : {pkg_dir}")
    print(f"  Release ZIP : {final_zip} ({zip_mb:.2f} MB)")
    print(f"  SHA-256     : {digest}")


if __name__ == "__main__":
    main()
