# -*- coding: utf-8 -*-
"""
Blue Glass Engine - Standalone Bilingual BYOA GUI/CLI Importer (BYOA_Importer.exe)
==================================================================================
Zero-Python-dependency graphical importer for legally owned Tsukihime (2000) copies.
Features:
  - Single-folder UX with automatic sibling game/ detection & hard engine-core guard
  - High-DPI safe layout (footer action bar packed bottom-first; never clipped!)
  - Live Chinese / English bilingual toggle (auto-detects OS locale)
  - Embedded Blue Glass Moon window icon
"""

import os
import re
import sys
import io
import queue
import ctypes
import locale
import threading
import subprocess
import traceback

if getattr(sys, "frozen", False):
    APP_ROOT = os.path.dirname(os.path.abspath(sys.executable))
    BUNDLE_DIR = getattr(sys, "_MEIPASS", APP_ROOT)
else:
    APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    BUNDLE_DIR = os.path.join(APP_ROOT, "Tsukihime_HD")
    sys.path.insert(0, os.path.join(APP_ROOT, "scripts"))

import byoa_import as imp


def detect_default_lang():
    try:
        if sys.platform == "win32":
            lid = ctypes.windll.kernel32.GetUserDefaultUILanguage()
            return "zh" if (lid & 0xFF) == 0x04 else "en"
    except Exception:
        pass
    try:
        loc = (locale.getlocale()[0] or "").lower()
        if loc.startswith("zh") or "chinese" in loc:
            return "zh"
    except Exception:
        pass
    return "en"


I18N = {
    "zh": {
        "win_title": "月姬 Classic HD · BYOA 资源导入工具",
        "eyebrow": "BLUE GLASS ENGINE  ·  BYOA IMPORTER",
        "heading": "月姬 Classic HD 资源导入工具",
        "subtitle": "选择本地原版《月姬 (2000)》目录，自动完成解包、剧本转译与高清标题合成。",
        "src_lbl": "原版《月姬》目录",
        "browse": "浏览...",
        "browse_src_title": "选择原版《月姬 (2000)》目录",
        "browse_eng_title": "选择游戏根目录（需包含 game/ui 文件夹）",
        "change_eng": "更改引擎目录",
        "eng_ok_sibling": "●  目标引擎已就绪：同级 game/",
        "eng_ok_path": "●  目标引擎已就绪：{path}",
        "eng_missing": "○  未检测到同级引擎核心（game/ui），请放回解压后的游戏根目录或点击右侧指定",
        "chk_wait_arc": "○  封包：等待选择原版目录",
        "chk_wait_scr": "○  剧本：等待选择原版目录",
        "chk_wait_bgm": "○  原声：等待选择原版目录",
        "arc_missing": "未检测到 arc.nsa / arc.sar 或散装 image 目录",
        "arc_ok": "已识别 {sources}",
        "arc_err": "封包读取失败：{err}",
        "scr_missing": "未检测到 0.txt 或 nscript.dat",
        "scr_ok": "{src}（{lang} / {enc}）",
        "bgm_missing": "未检测到原声音乐（可正常运行但无 BGM）",
        "bgm_ok": "已检测到 {n} / 10 首原声曲目",
        "qual_title": "画质模式",
        "qual_fast": "极速模式（纯 CPU，约 10 秒完成，兼容所有电脑，推荐）",
        "qual_hd": "AI 4× 超分模式（需 Vulkan 独显，耗时数分钟 · {hint}）",
        "hd_ready": "已检测到 Vulkan 超分工具",
        "hd_fallback": "未检测到工具（放入 tools/realesrgan/ 后可用）",
        "status_init": "请选择包含 arc.nsa 与 0.txt / nscript.dat 的原版目录。",
        "status_no_eng": "未检测到引擎核心目录（game/ui），请先确认本工具位于游戏根目录。",
        "status_ready": "检测通过，点击右下角「开始导入」即可自动完成配置。",
        "status_running": "正在导入并构建本地运行资产，请稍候...",
        "status_done": "导入完成，点击右下角「启动游戏」即可开始游玩。",
        "status_fail": "导入失败，请查看上方日志定位原因。",
        "btn_start": "开始导入",
        "btn_play": "启动游戏",
        "footer_note": "开源 BYOA 工具 · 仅读取本地正版文件",
        "dlg_no_eng_t": "缺少引擎目录",
        "dlg_no_eng_m": "未检测到引擎核心（game/ui），请将本工具放回解压后的游戏根目录再运行。",
        "dlg_bad_src_t": "目录无效",
        "dlg_bad_src_m": "请选择有效的原版《月姬 (2000)》目录。",
        "dlg_launch_t": "提示",
        "dlg_launch_m": "导入已完成，直接双击同目录下的 BlueGlassHD.exe 即可启动。",
        "lang_names": {"zh_hans": "简体中文", "zh_hant": "繁体中文", "ja": "日文原版", "en": "英文版"},
    },
    "en": {
        "win_title": "Tsukihime Classic HD · BYOA Asset Importer",
        "eyebrow": "BLUE GLASS ENGINE  ·  BYOA IMPORTER",
        "heading": "Tsukihime Classic HD Asset Importer",
        "subtitle": "Select your local Tsukihime (2000) folder to extract art, transpile script, and build HD title assets.",
        "src_lbl": "Tsukihime Folder",
        "browse": "Browse...",
        "browse_src_title": "Select Your Tsukihime (2000) Directory",
        "browse_eng_title": "Select Game Root Folder (containing game/ui)",
        "change_eng": "Change Target",
        "eng_ok_sibling": "●  Engine target ready: sibling game/",
        "eng_ok_path": "●  Engine target ready: {path}",
        "eng_missing": "○  Engine core (game/ui) not found beside importer. Place it in the game root or pick target.",
        "chk_wait_arc": "○  Archive: waiting for source folder",
        "chk_wait_scr": "○  Script: waiting for source folder",
        "chk_wait_bgm": "○  Audio: waiting for source folder",
        "arc_missing": "No arc.nsa / arc.sar archive or image/ folder found",
        "arc_ok": "Detected {sources}",
        "arc_err": "Archive read error: {err}",
        "scr_missing": "No 0.txt or nscript.dat script found",
        "scr_ok": "{src} ({lang} / {enc})",
        "bgm_missing": "No BGM tracks found (game still runs without music)",
        "bgm_ok": "Detected {n} / 10 soundtrack tracks",
        "qual_title": "Visual Mode",
        "qual_fast": "Fast Mode (CPU WebP, ~10 sec, works on all PCs, Recommended)",
        "qual_hd": "AI 4x Upscale (Vulkan GPU, several minutes · {hint})",
        "hd_ready": "Vulkan upscaler detected",
        "hd_fallback": "Not installed (place under tools/realesrgan/ to enable)",
        "status_init": "Select a Tsukihime (2000) folder containing arc.nsa and 0.txt / nscript.dat.",
        "status_no_eng": "Engine core (game/ui) not detected. Keep this tool inside the unzipped game root.",
        "status_ready": "Verification passed. Click 'Start Import' below to begin.",
        "status_running": "Importing and building local runtime assets, please wait...",
        "status_done": "Import complete! Click 'Launch Game' below to play.",
        "status_fail": "Import failed. Check the log above for details.",
        "btn_start": "Start Import",
        "btn_play": "Launch Game",
        "footer_note": "Open-Source BYOA Tool · Reads Local Files Only",
        "dlg_no_eng_t": "Missing Engine Directory",
        "dlg_no_eng_m": "Engine core (game/ui) not found. Move BYOA_Importer.exe back into the unzipped game root.",
        "dlg_bad_src_t": "Invalid Folder",
        "dlg_bad_src_m": "Please select a valid Tsukihime (2000) installation folder.",
        "dlg_launch_t": "Ready",
        "dlg_launch_m": "Import complete. Double-click BlueGlassHD.exe in this folder to start.",
        "lang_names": {"zh_hans": "Simplified Chinese", "zh_hant": "Traditional Chinese", "ja": "Japanese", "en": "English"},
    },
}


def is_valid_engine_dir(path):
    """Verify target directory contains the real open-source engine core (game/ui + game/core)."""
    if not path or not os.path.isdir(path):
        return False
    return (
        os.path.isdir(os.path.join(path, "game", "ui"))
        and os.path.isdir(os.path.join(path, "game", "core"))
    )


def detect_engine_dir():
    """Auto-locate engine root: flat release folder first (game/ beside exe), then dev Tsukihime_HD/."""
    for cand in (
        APP_ROOT,
        os.path.join(APP_ROOT, "Tsukihime_HD"),
        os.path.dirname(APP_ROOT),
    ):
        if is_valid_engine_dir(cand):
            return os.path.abspath(cand)
    return ""


def detect_game_launcher(engine_dir):
    """Locate runnable player executable (flat BlueGlassHD.exe first, then dev SDK renpy.exe)."""
    if not engine_dir:
        return None
    for exe_name in ("BlueGlassHD.exe", "Tsukihime_HD.exe"):
        for base in (engine_dir, APP_ROOT):
            cand = os.path.join(base, exe_name)
            if os.path.isfile(cand):
                return [cand]
    for base in (APP_ROOT, os.path.dirname(engine_dir)):
        sdk_exe = os.path.join(base, "tools", "renpy_sdk", "renpy-8.5.3-sdk", "renpy.exe")
        if os.path.isfile(sdk_exe):
            return [sdk_exe, engine_dir]
    return None


def inspect_source_dir(src_dir, lang="zh"):
    """Read-only quick pre-check of a candidate Tsukihime (2000) directory."""
    tr = I18N[lang]
    result = {
        "valid": False,
        "archive_ok": False,
        "archive_msg": tr["arc_missing"],
        "script_ok": False,
        "script_msg": tr["scr_missing"],
        "bgm_count": 0,
        "bgm_msg": tr["bgm_missing"],
    }
    if not src_dir or not os.path.isdir(src_dir):
        return result

    try:
        vfs = imp.NScripterVFS(src_dir)
        if vfs.entries:
            result["archive_ok"] = True
            result["archive_msg"] = tr["arc_ok"].format(sources=", ".join(vfs.mounted_sources))
    except Exception as e:
        result["archive_msg"] = tr["arc_err"].format(err=e)

    try:
        _, enc, slang, s_src = imp.discover_and_decode_script(src_dir)
        result["script_ok"] = True
        result["script_msg"] = tr["scr_ok"].format(
            src=s_src, lang=tr["lang_names"].get(slang, slang), enc=enc
        )
    except Exception:
        pass

    search_dirs = [src_dir]
    for sub in os.listdir(src_dir):
        if sub.lower() in ("bgm", "cd", "music", "audio") and os.path.isdir(os.path.join(src_dir, sub)):
            search_dirs.append(os.path.join(src_dir, sub))
    found = set()
    for sd in search_dirs:
        for fn in os.listdir(sd):
            full = os.path.join(sd, fn)
            if not os.path.isfile(full):
                continue
            ext = os.path.splitext(fn)[1].lower()
            if ext not in (".wav", ".flac", ".ogg", ".mp3"):
                continue
            stem = os.path.splitext(fn)[0].lower()
            m = re.match(r"^(?:track|bgm|cd|m)?[_-]?0*(\d{1,2})$", stem)
            if m and 1 <= int(m.group(1)) <= 12:
                found.add(int(m.group(1)))
    bgm_n = min(10, len(found))
    result["bgm_count"] = bgm_n
    if bgm_n > 0:
        result["bgm_msg"] = tr["bgm_ok"].format(n=bgm_n)

    result["valid"] = bool(result["archive_ok"] and result["script_ok"])
    return result


class _StreamQueueWriter(io.TextIOBase):
    def __init__(self, q):
        self.q = q
        self._buf = ""

    def write(self, s):
        if not s:
            return 0
        self._buf += s
        while "\n" in self._buf:
            line, self._buf = self._buf.split("\n", 1)
            self.q.put(("log", line))
        return len(s)

    def flush(self):
        if self._buf:
            self.q.put(("log", self._buf))
            self._buf = ""


def launch_gui():
    if sys.platform == "win32":
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass

    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox

    BG_MAIN = "#121822"
    BG_CARD = "#1b2433"
    BG_INPUT = "#0f151e"
    BORDER = "#2d3b50"
    FG_PRI = "#eef4fa"
    FG_SEC = "#93a5bb"
    ACCENT = "#8ab8e6"
    MINT = "#7ce0be"
    ROSE = "#e89ca8"
    GOLD = "#dec894"

    state = {"lang": detect_default_lang(), "active": False, "imported": False}

    def T(key):
        return I18N[state["lang"]][key]

    root = tk.Tk()
    root.title(T("win_title"))
    root.configure(bg=BG_MAIN)

    engine_dir_init = detect_engine_dir()
    for ico_cand in (
        os.path.join(BUNDLE_DIR, "icon.ico"),
        os.path.join(engine_dir_init, "icon.ico") if engine_dir_init else "",
        os.path.join(APP_ROOT, "icon.ico"),
    ):
        if ico_cand and os.path.isfile(ico_cand):
            try:
                root.iconbitmap(ico_cand)
                break
            except Exception:
                pass

    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except Exception:
        pass
    style.configure(
        "Mist.Horizontal.TProgressbar",
        troughcolor=BG_INPUT,
        background=ACCENT,
        bordercolor=BORDER,
        lightcolor=ACCENT,
        darkcolor=ACCENT,
        thickness=9,
    )

    ui_font = ("Microsoft YaHei UI", 10)
    ui_bold = ("Microsoft YaHei UI", 10, "bold")
    ui_title = ("Microsoft YaHei UI", 14, "bold")
    ui_small = ("Microsoft YaHei UI", 9)
    mono_font = ("Consolas", 9)

    src_var = tk.StringVar(value="")
    tgt_var = tk.StringVar(value=engine_dir_init)
    qual_var = tk.StringVar(value="fast")
    status_var = tk.StringVar(value=T("status_init"))

    msg_q = queue.Queue()
    esrgan_exe, _ = imp._find_realesrgan()

    # --- Header + Top-Right Bilingual Switcher (中文 | EN) ---
    hdr = tk.Frame(root, bg=BG_MAIN, padx=24, pady=12)
    hdr.pack(side="top", fill="x")

    hdr_top = tk.Frame(hdr, bg=BG_MAIN)
    hdr_top.pack(fill="x")
    lbl_eye = tk.Label(hdr_top, text=T("eyebrow"), font=("Segoe UI", 9, "bold"), fg=ACCENT, bg=BG_MAIN)
    lbl_eye.pack(side="left", anchor="w")

    lang_box = tk.Frame(hdr_top, bg=BG_INPUT, highlightbackground=BORDER, highlightthickness=1, padx=2, pady=2)
    lang_box.pack(side="right")

    lbl_heading = tk.Label(hdr, text=T("heading"), font=ui_title, fg=FG_PRI, bg=BG_MAIN)
    lbl_heading.pack(anchor="w", pady=(2, 1))
    lbl_sub = tk.Label(hdr, text=T("subtitle"), font=ui_small, fg=FG_SEC, bg=BG_MAIN)
    lbl_sub.pack(anchor="w")

    # --- FOOTER PACKED BOTTOM-FIRST (GUARANTEED ALWAYS VISIBLE AT ANY DPI!) ---
    ftr_wrap = tk.Frame(root, bg="#161f2d")
    ftr_wrap.pack(side="bottom", fill="x")
    tk.Frame(ftr_wrap, bg=BORDER, height=1).pack(fill="x")
    ftr = tk.Frame(ftr_wrap, bg="#161f2d", padx=24, pady=12)
    ftr.pack(fill="x")

    lbl_footer = tk.Label(ftr, text=T("footer_note"), font=ui_small, fg=FG_SEC, bg="#161f2d")
    lbl_footer.pack(side="left", pady=4)

    def on_launch_game():
        cmd = detect_game_launcher(tgt_var.get().strip())
        if not cmd:
            messagebox.showinfo(T("dlg_launch_t"), T("dlg_launch_m"))
            return
        subprocess.Popen(cmd)
        root.destroy()

    btn_play = tk.Button(
        ftr, text=T("btn_play"), font=ui_bold,
        bg="#234942", fg="#e6fff6", disabledforeground="#627874",
        activebackground="#2f6258", activeforeground="#ffffff",
        relief="flat", padx=20, pady=7, cursor="hand2", state="disabled",
        command=on_launch_game,
    )
    btn_play.pack(side="right", padx=(10, 0))

    # --- Card 1: Single-Folder Source Picker + Auto-Detected Engine Status ---
    c1 = tk.Frame(root, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1, padx=16, pady=12)
    c1.pack(side="top", fill="x", padx=24, pady=(0, 10))
    c1.columnconfigure(1, weight=1)

    lbl_src = tk.Label(c1, text=T("src_lbl"), font=ui_bold, fg=FG_PRI, bg=BG_CARD, width=14, anchor="w")
    lbl_src.grid(row=0, column=0, sticky="w", pady=2)
    ent_src = tk.Entry(
        c1, textvariable=src_var, font=ui_font, bg=BG_INPUT, fg=FG_PRI,
        insertbackground=FG_PRI, relief="flat", highlightbackground=BORDER, highlightthickness=1,
    )
    ent_src.grid(row=0, column=1, sticky="ew", padx=(8, 10), pady=2, ipady=4)

    chk_labels = {}
    btn_start_ref = {"btn": None}

    def update_ready_state():
        eng_path = tgt_var.get().strip()
        eng_ok = is_valid_engine_dir(eng_path)
        if eng_ok:
            if os.path.abspath(eng_path) == os.path.abspath(APP_ROOT):
                eng_lbl.config(text=T("eng_ok_sibling"), fg=MINT)
            else:
                eng_lbl.config(text=T("eng_ok_path").format(path=eng_path), fg=MINT)
        else:
            eng_lbl.config(text=T("eng_missing"), fg=ROSE)

        raw_src = src_var.get().strip()
        if not raw_src:
            chk_labels["archive"].config(text=T("chk_wait_arc"), fg=FG_SEC)
            chk_labels["script"].config(text=T("chk_wait_scr"), fg=FG_SEC)
            chk_labels["bgm"].config(text=T("chk_wait_bgm"), fg=FG_SEC)
            info = {"valid": False}
        else:
            info = inspect_source_dir(raw_src, lang=state["lang"])
            chk_labels["archive"].config(
                text=("●  " if info["archive_ok"] else "○  ") + info["archive_msg"],
                fg=(MINT if info["archive_ok"] else FG_SEC),
            )
            chk_labels["script"].config(
                text=("●  " if info["script_ok"] else "○  ") + info["script_msg"],
                fg=(MINT if info["script_ok"] else FG_SEC),
            )
            chk_labels["bgm"].config(
                text=("●  " if info["bgm_count"] > 0 else "○  ") + info["bgm_msg"],
                fg=(MINT if info["bgm_count"] >= 10 else (GOLD if info["bgm_count"] > 0 else FG_SEC)),
            )

        if not state["active"] and btn_start_ref["btn"] is not None:
            can_go = bool(eng_ok and info["valid"])
            btn_start_ref["btn"].config(
                state=("normal" if can_go else "disabled"),
                bg=("#2e5d8c" if can_go else "#223042"),
            )
            if not state["imported"]:
                if not eng_ok:
                    status_var.set(T("status_no_eng"))
                elif info["valid"]:
                    status_var.set(T("status_ready"))
                else:
                    status_var.set(T("status_init"))

    def browse_src():
        d = filedialog.askdirectory(title=T("browse_src_title"))
        if d:
            state["imported"] = False
            src_var.set(os.path.normpath(d))
            update_ready_state()

    def browse_eng():
        d = filedialog.askdirectory(title=T("browse_eng_title"), initialdir=tgt_var.get() or APP_ROOT)
        if d:
            tgt_var.set(os.path.normpath(d))
            update_ready_state()

    btn_b_src = tk.Button(
        c1, text=T("browse"), font=ui_small, bg="#263448", fg=FG_PRI,
        activebackground="#334660", activeforeground="#ffffff",
        relief="flat", padx=14, pady=4, cursor="hand2", command=browse_src,
    )
    btn_b_src.grid(row=0, column=2, pady=2)

    chk_box = tk.Frame(c1, bg=BG_INPUT, padx=12, pady=7, highlightbackground=BORDER, highlightthickness=1)
    chk_box.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(8, 6))
    for key, tkey in (("archive", "chk_wait_arc"), ("script", "chk_wait_scr"), ("bgm", "chk_wait_bgm")):
        lbl = tk.Label(chk_box, text=T(tkey), font=ui_small, fg=FG_SEC, bg=BG_INPUT, anchor="w")
        lbl.pack(fill="x", pady=1)
        chk_labels[key] = lbl

    eng_row = tk.Frame(c1, bg=BG_CARD)
    eng_row.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(2, 0))
    eng_lbl = tk.Label(eng_row, text="", font=ui_small, fg=MINT, bg=BG_CARD, anchor="w")
    eng_lbl.pack(side="left", fill="x", expand=True)
    btn_b_eng = tk.Button(
        eng_row, text=T("change_eng"), font=ui_small, bg=BG_CARD, fg=FG_SEC,
        activebackground=BG_CARD, activeforeground=FG_PRI, relief="flat", cursor="hand2", command=browse_eng,
    )
    btn_b_eng.pack(side="right")

    src_var.trace_add("write", lambda *_: update_ready_state())

    # --- Card 2: Quality Mode ---
    c2 = tk.Frame(root, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1, padx=16, pady=10)
    c2.pack(side="top", fill="x", padx=24, pady=(0, 10))
    lbl_qual = tk.Label(c2, text=T("qual_title"), font=ui_bold, fg=FG_PRI, bg=BG_CARD)
    lbl_qual.pack(anchor="w", pady=(0, 4))

    rb_fast = tk.Radiobutton(
        c2, text=T("qual_fast"), variable=qual_var, value="fast", font=ui_small,
        fg=FG_PRI, bg=BG_CARD, selectcolor=BG_INPUT, activebackground=BG_CARD, activeforeground="#ffffff",
    )
    rb_fast.pack(anchor="w")

    rb_hd = tk.Radiobutton(
        c2, text=T("qual_hd").format(hint=T("hd_ready") if esrgan_exe else T("hd_fallback")),
        variable=qual_var, value="hd", font=ui_small,
        fg=(FG_PRI if esrgan_exe else FG_SEC), disabledforeground="#5c6e84", bg=BG_CARD, selectcolor=BG_INPUT,
        activebackground=BG_CARD, activeforeground="#ffffff",
        state=("normal" if esrgan_exe else "disabled"),
    )
    rb_hd.pack(anchor="w", pady=(2, 0))

    # --- Card 3: Progress & Compact Log Console (fills remaining middle space) ---
    c3 = tk.Frame(root, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1, padx=16, pady=10)
    c3.pack(side="top", fill="both", expand=True, padx=24, pady=(0, 10))

    tk.Label(c3, textvariable=status_var, font=ui_small, fg=ACCENT, bg=BG_CARD, anchor="w").pack(fill="x", pady=(0, 6))
    pbar = ttk.Progressbar(c3, style="Mist.Horizontal.TProgressbar", mode="determinate", maximum=100, value=0)
    pbar.pack(fill="x", pady=(0, 6))

    log_txt = tk.Text(
        c3, height=5, font=mono_font, bg=BG_INPUT, fg="#cdd9e8",
        relief="flat", state="disabled", wrap="word", padx=8, pady=5,
    )
    log_txt.pack(fill="both", expand=True)

    def append_log(line):
        log_txt.config(state="normal")
        log_txt.insert("end", line + "\n")
        log_txt.see("end")
        log_txt.config(state="disabled")
        m_sub = re.search(r"\[3/6\]\s*Progress:\s*\d+/\d+\s*\((\d+)%\)", line)
        if m_sub:
            pbar["value"] = 45 + int(int(m_sub.group(1)) * 0.25)
            return
        for step_i in range(1, 7):
            if f"[{step_i}/6]" in line:
                step_pcts = {1: 15, 2: 30, 3: 45, 4: 75, 5: 85, 6: 92}
                pbar["value"] = max(int(pbar["value"]), step_pcts[step_i])

    def worker_run(src_dir, target_proj, quality):
        old_out, old_err = sys.stdout, sys.stderr
        writer = _StreamQueueWriter(msg_q)
        sys.stdout = writer
        sys.stderr = writer
        try:
            target_game = os.path.join(target_proj, "game")
            vfs = imp.NScripterVFS(src_dir)
            if not vfs.entries:
                raise RuntimeError("No NScripter archive or image directory found.")
            print(f"[1/6] Mounted archive ({len(vfs.entries)} files): {', '.join(vfs.mounted_sources)}")

            script_text, enc, lang, script_src = imp.discover_and_decode_script(src_dir)
            print(f"      Script: {script_src} | encoding={enc} | lang={lang}")

            audio_ext_map = imp.import_audio(vfs, src_dir, target_game)
            imp.import_images(vfs, target_game, quality=quality)
            imp.generate_image_definitions(target_game)
            imp.synthesize_user_derived_gui(vfs, target_game)

            print("[6/6] Transpiling story scripts...")
            t = imp.transpiler.TsukihimeASTTranspiler(
                out_game_dir=target_game,
                script_text=script_text,
                edition_lang=lang,
                audio_ext_map=audio_ext_map,
            )
            t.transpile_all()
            writer.flush()
            msg_q.put(("done", True))
        except Exception as e:
            print(f"[ERROR] {e}")
            print(traceback.format_exc())
            writer.flush()
            msg_q.put(("done", False))
        finally:
            sys.stdout = old_out
            sys.stderr = old_err

    def on_start_import():
        src_dir = src_var.get().strip()
        target_proj = tgt_var.get().strip()
        if not is_valid_engine_dir(target_proj):
            messagebox.showerror(T("dlg_no_eng_t"), T("dlg_no_eng_m"))
            return
        if not os.path.isdir(src_dir):
            messagebox.showerror(T("dlg_bad_src_t"), T("dlg_bad_src_m"))
            return
        state["active"] = True
        state["imported"] = False
        btn_start.config(state="disabled", bg="#223042")
        btn_play.config(state="disabled")
        btn_b_src.config(state="disabled")
        btn_b_eng.config(state="disabled")
        pbar["value"] = 5
        status_var.set(T("status_running"))
        log_txt.config(state="normal")
        log_txt.delete("1.0", "end")
        log_txt.config(state="disabled")

        th = threading.Thread(target=worker_run, args=(src_dir, target_proj, qual_var.get()), daemon=True)
        th.start()

    btn_start = tk.Button(
        ftr, text=T("btn_start"), font=ui_bold,
        bg="#223042", fg="#ffffff", disabledforeground="#7e94ae",
        activebackground="#3a71a8", activeforeground="#ffffff",
        relief="flat", padx=24, pady=7, cursor="hand2", state="disabled",
        command=on_start_import,
    )
    btn_start.pack(side="right")
    btn_start_ref["btn"] = btn_start

    # Language switch buttons inside top-right pill
    def apply_language(new_lang):
        state["lang"] = new_lang
        root.title(T("win_title"))
        lbl_eye.config(text=T("eyebrow"))
        lbl_heading.config(text=T("heading"))
        lbl_sub.config(text=T("subtitle"))
        lbl_src.config(text=T("src_lbl"))
        btn_b_src.config(text=T("browse"))
        btn_b_eng.config(text=T("change_eng"))
        lbl_qual.config(text=T("qual_title"))
        rb_fast.config(text=T("qual_fast"))
        rb_hd.config(text=T("qual_hd").format(hint=T("hd_ready") if esrgan_exe else T("hd_fallback")))
        btn_start.config(text=T("btn_start"))
        btn_play.config(text=T("btn_play"))
        lbl_footer.config(text=T("footer_note"))
        btn_lang_zh.config(
            bg=("#2e5d8c" if new_lang == "zh" else BG_INPUT),
            fg=("#ffffff" if new_lang == "zh" else FG_SEC),
        )
        btn_lang_en.config(
            bg=("#2e5d8c" if new_lang == "en" else BG_INPUT),
            fg=("#ffffff" if new_lang == "en" else FG_SEC),
        )
        if state["imported"]:
            status_var.set(T("status_done"))
        elif state["active"]:
            status_var.set(T("status_running"))
        update_ready_state()

    btn_lang_zh = tk.Button(
        lang_box, text="中文", font=ui_small, relief="flat", padx=10, pady=2, cursor="hand2",
        activebackground="#3a71a8", activeforeground="#ffffff",
        command=lambda: apply_language("zh"),
    )
    btn_lang_zh.pack(side="left")
    btn_lang_en = tk.Button(
        lang_box, text="EN", font=ui_small, relief="flat", padx=10, pady=2, cursor="hand2",
        activebackground="#3a71a8", activeforeground="#ffffff",
        command=lambda: apply_language("en"),
    )
    btn_lang_en.pack(side="left")

    def poll_queue():
        try:
            while True:
                kind, payload = msg_q.get_nowait()
                if kind == "log":
                    append_log(payload)
                elif kind == "done":
                    state["active"] = False
                    btn_b_src.config(state="normal")
                    btn_b_eng.config(state="normal")
                    if payload:
                        state["imported"] = True
                        pbar["value"] = 100
                        status_var.set(T("status_done"))
                        btn_play.config(state="normal", bg="#2a6054")
                        btn_start.config(state="normal", bg="#2e5d8c")
                    else:
                        status_var.set(T("status_fail"))
                        btn_start.config(state="normal", bg="#2e5d8c")
        except queue.Empty:
            pass
        root.after(80, poll_queue)

    apply_language(state["lang"])

    # High-DPI safe auto-sizing & centering (prevents clipping at 125% / 150% / 200% scaling!)
    root.update_idletasks()
    req_w = max(760, root.winfo_reqwidth() + 24)
    req_h = max(620, root.winfo_reqheight() + 24)
    scr_w = root.winfo_screenwidth()
    scr_h = root.winfo_screenheight()
    win_w = min(req_w, max(680, scr_w - 60))
    win_h = min(req_h, max(540, scr_h - 80))
    pos_x = max(0, (scr_w - win_w) // 2)
    pos_y = max(0, (scr_h - win_h) // 2)
    root.geometry(f"{win_w}x{win_h}+{pos_x}+{pos_y}")
    root.minsize(min(win_w, 720), min(win_h, 540))

    root.after(80, poll_queue)
    root.mainloop()


def main():
    if len(sys.argv) > 1:
        if sys.stdout is None:
            sys.stdout = open(os.devnull, "w", encoding="utf-8")
        elif hasattr(sys.stdout, "reconfigure"):
            try:
                sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass
        if sys.stderr is None:
            sys.stderr = open(os.devnull, "w", encoding="utf-8")
        elif hasattr(sys.stderr, "reconfigure"):
            try:
                sys.stderr.reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass
        if "--target" not in sys.argv and not any(a.startswith("--target=") for a in sys.argv):
            eng = detect_engine_dir()
            if not eng:
                sys.stderr.write(
                    "[ERROR] Engine core (game/ui and game/core) not found beside BYOA_Importer. "
                    "Keep it in the unzipped game root or pass --target.\n"
                )
                sys.exit(2)
            sys.argv.extend(["--target", eng])
        imp.main()
    else:
        launch_gui()


if __name__ == "__main__":
    main()
