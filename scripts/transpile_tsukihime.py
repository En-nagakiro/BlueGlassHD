# -*- coding: utf-8 -*-
r"""
Tsukihime Classic HD - AST NScripter -> Ren'Py 8.5.3 NVL Transpiler
===================================================================
Clean-room rewrite targeting Tsukihime_HD/game/:
  - 100% faithful full-screen NVL pacing (\ page clear, @ inline click-wait, br breaks, #color)
  - 100% uncensored original 2000 script (zero broken H-scene guards or fall-through bugs)
  - True cross-playthrough persistent progression (cleared / clear_* / ark_normalcleared)
  - Dynamic 3-slot standing sprite engine (tsuki_ld / tsuki_cl, zero hardcoded hide aki/his)
  - Complete NScripter transitions (crossfade/shutter/cartain/nowaitdisp)
  - Complete 3-layer chapter title cards ($phasebg + $phasetitle_a + $phasetitle_b)
  - Scene-layer monochrome MatrixColor (never obscures NVL text)
  - Fixed waveloop ambient channel, staffrollwait 4s pacing, if %flgE>=1 skip branching,
    and clean endofplay -> return (eliminates title_tochu infinite freeze loop)
  - Automatic mathematical Bad-End choice graph extraction for optional Guide HUD
"""

import os
import re
import sys
from collections import defaultdict, deque

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_0TXT = os.environ.get("TSUKIHIME_SCRIPT", "")
FALLBACK_0TXT = ""
OUT_GAME = os.path.join(ROOT, "Tsukihime_HD", "game")

AUDIO_MAP = {
    "m1": "01.wav", "m2": "02.wav", "m3": "03.wav", "m4": "04.wav", "m5": "05.wav",
    "m6": "06.wav", "m7": "07.wav", "m8": "08.wav", "m9": "09.wav", "m10": "10.wav",
    "se0": "se_01.wav", "se1": "se_02.wav", "se2": "se_03.wav", "se3": "se_04.wav",
    "se4": "se_05.wav", "se5": "se_06.wav", "se6": "se_07.wav", "se7": "se_08.wav",
    "se8": "se_09.wav", "se9": "se_10.wav", "se10": "se_11.wav", "se11": "se_12.wav",
    "se12": "se_13.wav", "se13": "se_14.wav", "se14": "se_15.wav",
}

PERSISTENT_VARS = {
    "execution_cnt", "cleared", "ark_normalcleared",
    "clear_ark", "clear_ciel", "clear_akiha", "clear_kohaku", "clear_hisui",
    "clear_ark_true", "clear_ark_good",
    "clear_ciel_true", "clear_ciel_good",
    "clear_akiha_true", "clear_akiha_good",
    "clear_kohaku_true", "clear_kohaku_good",
    "clear_hisui_true", "clear_hisui_good",
}

DEAD_SYSTEM_LABELS = {
    "define", "start", "title", "title_tochu", "title2", "gamestart_menu",
    "option", "gallery", "gallery1", "gallery2", "endinglist", "gameopt",
    "ark_gallery", "ciel_gallery", "akiha_gallery", "hisui_gallery", "kohaku_gallery",
    "ark_gallery_check", "ciel_gallery_check", "akiha_gallery_check",
    "hisui_gallery_check", "kohaku_gallery_check",
    "imagemode", "imagemode_c", "imagemode_k", "imagemode_h", "imagemode_a",
    "checks", "next1", "next2", "next3",
    "regard_update", "regard_check", "normal_effectspeed", "velocity_effectspeed",
    "left_phase", "right_phase", "center_phase",
}

ENGINE_COMMANDS_TO_IGNORE = {
    "!sd", "resettimer", "autoclick", "setwindow", "setcursor", "windoweffect",
    "lsp", "csp", "msp", "print", "btn", "btndef", "btnwait", "systemcall",
    "rubyon", "rubyparent", "defsub", "kinsoku", "humanorder", "isskip",
    "caption", "versionstr", "numalias", "stralias", "nsa", "effect",
    "effectblank", "mp3fadeout", "clickstr", "menusetwindow", "menuselectcolor",
    "rmenu", "savenumber", "savename", "lookbackbutton", "lookbackcolor",
    "globalon", "filelog", "game", "selectcolor", "cmp", "csel", "tablegoto",
    "fchk", "bar", "barclear", "prnum", "prnumclear", "notif", "selgosub",
}

TERMINOLOGY_REPLACEMENTS = [
    (r"阿鲁奎特", "爱尔奎特"),
    (r"雪儿", "希耶尔"),
    (r"Siel学姐", "希耶尔学姐"),
    (r"Siel", "希耶尔"),
    (r"\bakiha\s*被转入", "秋叶被转入"),
]

COMMENTARY_PATTERNS = [
    r"[（\(][^）\)]*(?:吐槽|我去|那你怎么|因为跟你共享生命|当然，酱料是肉酱|而且是坐车|·＿·|无语|日语里抱有上床|原文为卡欧斯)[^）\)]*[）\)]",
    r"[（\(](?:注|译注|原注|按)：[^）\)]+[）\)]",
    r"[（\(][^）\)]*(?:笑顔|笑い|私服|困惑|照れ|企んで|変な顔|怒り|基本)[^）\)]*[）\)]",
    r"（·＿·）",
]


def map_var(v):
    v = v.strip()
    if not v:
        return "var_empty"
    if v in PERSISTENT_VARS:
        return f"persistent.{v}"
    return f"var_{v}" if v[0].isdigit() else v


def normalize_transition(raw_trans):
    if not raw_trans:
        return "crossfade_mid"
    t = raw_trans.split(";")[0].strip().rstrip("\\").lstrip("%")
    if t.startswith("type_"):
        t = t[5:]
    return t if t else "crossfade_mid"


def resolve_audio_stem(token):
    token = token.strip().strip('"')
    if token.startswith("*") and token[1:].isdigit():
        return f"{int(token[1:]):02d}"
    if token in AUDIO_MAP:
        return os.path.splitext(AUDIO_MAP[token])[0].lower()
    bname = os.path.basename(token.replace("\\", "/"))
    return os.path.splitext(bname)[0].lower()


def resolve_audio(token, audio_ext_map=None):
    base_low = resolve_audio_stem(token)
    if audio_ext_map and base_low in audio_ext_map:
        return audio_ext_map[base_low]
    return f"{base_low}.wav"


def sanitize_text(text, apply_zh_fixes=True):
    cleaned = text
    if apply_zh_fixes:
        for pat in COMMENTARY_PATTERNS:
            cleaned = re.sub(pat, "", cleaned)
        for src, dst in TERMINOLOGY_REPLACEMENTS:
            cleaned = re.sub(src, dst, cleaned)
        cleaned = re.sub(r"ー{2,}", "——", cleaned)
        cleaned = re.sub(r"([\u4e00-\u9fff])ー", r"\1～", cleaned)
    cleaned = re.sub(r"[ \t]+", " ", cleaned)
    return cleaned.strip()


def escape_renpy_text(text):
    # Escape Ren'Py special interpolation / tag / format characters safely
    t = text.replace("\\", "\\\\")
    t = t.replace('"', '\\"')
    t = t.replace("[", "[[")
    t = t.replace("{", "{{")
    t = t.replace("%", "%%")
    return t


def convert_inline_nscripter_tags(escaped_text):
    """Convert NScripter inline wait/delay tags (!w2000, !d500) to Ren'Py {w=sec} and strip stray !s speed tags."""
    def _repl_wait(m):
        try:
            ms = int(m.group(1))
        except ValueError:
            ms = 500
        sec = max(0.05, round(ms / 1000.0, 2))
        return f"{{w={sec}}}"

    t = re.sub(r"![wd](\d+)", _repl_wait, escaped_text, flags=re.IGNORECASE)
    t = re.sub(r"!s(?:\d+|d)", "", t, flags=re.IGNORECASE)
    return t


def estimate_visual_lines(text, chars_per_line=34):
    clean = re.sub(r"![wd]\d+|!s(?:\d+|d)", "", text, flags=re.IGNORECASE)
    total = 0
    for seg in clean.split("\n"):
        if not seg.strip():
            total += 1
        else:
            total += max(1, (len(seg) + chars_per_line - 1) // chars_per_line)
    return total


def decode_nscripter_bytes(raw_bytes, is_encrypted=False):
    """
    Decode NScripter script bytes (supporting encrypted nscript.dat ^ 0x84 and plain 0.txt)
    with automatic multi-edition encoding & language detection (UTF-8 / GB18030 / CP932 / Big5).
    """
    if is_encrypted:
        raw_bytes = bytes(b ^ 0x84 for b in raw_bytes)

    # 1. Exact UTF-8 BOM or valid clean UTF-8
    if raw_bytes.startswith(b"\xef\xbb\xbf"):
        txt = raw_bytes[3:].decode("utf-8", errors="replace")
        enc = "utf-8-sig"
    else:
        try:
            txt = raw_bytes.decode("utf-8")
            enc = "utf-8"
        except UnicodeDecodeError:
            # Score GB18030 (SC) vs CP932 (JP) vs Big5 (TC) on a representative mid-script sample
            sample = raw_bytes[len(raw_bytes) // 4 : len(raw_bytes) // 4 + 120000]
            scores = {}
            for cand in ("gb18030", "cp932", "big5"):
                dec = sample.decode(cand, errors="replace")
                rep_pen = dec.count("\ufffd") * 8
                # Kana strongly indicates Japanese Shift-JIS; common SC punctuation/chars indicate GB18030
                kana = sum(1 for c in dec if "\u3040" <= c <= "\u30ff")
                cjk = sum(1 for c in dec if "\u4e00" <= c <= "\u9fff")
                sc_hits = sum(dec.count(ch) for ch in ("的", "了", "这", "说", "们", "远", "爱"))
                tc_hits = sum(dec.count(ch) for ch in ("這", "說", "們", "遠", "愛", "為", "嗎"))
                jp_hits = sum(dec.count(ch) for ch in ("の", "た", "て", "に", "は", "を", "が", "だ"))
                if cand == "cp932":
                    scores[cand] = kana * 4 + jp_hits * 8 + cjk * 0.3 - rep_pen
                elif cand == "gb18030":
                    scores[cand] = sc_hits * 10 + cjk * 0.5 - rep_pen
                else:
                    scores[cand] = tc_hits * 10 + cjk * 0.4 - rep_pen
            enc = max(scores, key=scores.get)
            txt = raw_bytes.decode(enc, errors="replace")

    # Classify script language for safe punctuation / terminology handling
    mid = txt[len(txt) // 4 : len(txt) // 4 + 60000]
    kana_cnt = sum(1 for c in mid if "\u3040" <= c <= "\u30ff")
    cjk_cnt = sum(1 for c in mid if "\u4e00" <= c <= "\u9fff")
    latin_cnt = sum(1 for c in mid if "a" <= c.lower() <= "z")
    if kana_cnt > 1500 and kana_cnt > cjk_cnt * 0.35:
        lang = "ja"
    elif cjk_cnt > 1200:
        lang = "zh_hant" if enc == "big5" else "zh_hans"
    elif latin_cnt > cjk_cnt * 3:
        lang = "en"
    else:
        lang = "zh_hans"
    return txt, enc, lang


class TsukihimeASTTranspiler:
    def __init__(self, script_path=None, out_game_dir=None, script_text=None,
                 edition_lang=None, audio_ext_map=None):
        self.script_path = script_path
        self.out_game_dir = out_game_dir or OUT_GAME
        self.script_text = script_text
        self.edition_lang = edition_lang or "zh_hans"
        self.detected_encoding = "utf-8"
        self.audio_ext_map = audio_ext_map or {}
        self.labels = {}
        self.label_order = []
        self.local_variables = set()
        self.bad_end_menu_indices = {}  # (f_label, choice_idx) -> True
        self.all_menus = {}             # f_label -> [(choice_text, target_label)]
        self.load_and_parse()
        self.analyze_bad_end_choices()

    def load_and_parse(self):
        if self.script_text is None:
            print(f"[1/4] Reading original script: {self.script_path} ...")
            raw_bytes = open(self.script_path, "rb").read()
            is_enc = os.path.basename(self.script_path).lower() == "nscript.dat"
            self.script_text, self.detected_encoding, auto_lang = decode_nscripter_bytes(raw_bytes, is_encrypted=is_enc)
            if not self.edition_lang:
                self.edition_lang = auto_lang
            else:
                self.edition_lang = auto_lang
            print(f"      Detected encoding={self.detected_encoding}, edition_lang={self.edition_lang}, encrypted={is_enc}")
        raw_lines = self.script_text.splitlines()

        current_label = None
        current_block = []

        for line in raw_lines:
            stripped = line.strip()
            if stripped.startswith("*"):
                lbl_name = stripped[1:].split()[0].replace("*", "").lower()
                if lbl_name == "define":
                    current_label = "define"
                    continue
                if lbl_name.startswith("skip"):
                    if current_label and current_label != "define":
                        current_block.append(line)
                    continue
                if current_label and current_label != "define":
                    self.labels[current_label] = current_block
                current_label = lbl_name
                if lbl_name not in self.labels:
                    self.label_order.append(lbl_name)
                current_block = []
            else:
                if current_label and current_label != "define":
                    current_block.append(line)

        if current_label and current_label != "define":
            self.labels[current_label] = current_block

        print(f"      Parsed {len(self.labels)} labels ({len(raw_lines)} lines).")

    def analyze_bad_end_choices(self):
        """Mathematically compute every choice trap that cannot reach any of the 9 endings."""
        f_edges = defaultdict(list)
        good_end_fs = set()
        for lbl, lines in self.labels.items():
            if lbl in DEAD_SYSTEM_LABELS:
                continue
            i = 0
            while i < len(lines):
                s = lines[i].strip()
                i += 1
                if not s or s.startswith(";"):
                    continue
                if s.startswith("inc %clear"):
                    good_end_fs.add(lbl)
                elif s.startswith("goto "):
                    tgt = s.split("*")[-1].strip().split()[0].lower()
                    f_edges[lbl].append(tgt)
                elif s.startswith("if "):
                    m = re.search(r"if\s+(.+)\s+goto\s+\*([a-zA-Z0-9_]+)", s)
                    if m:
                        f_edges[lbl].append(m.group(2).lower())
                elif s.startswith("select ") or s.startswith("select\t"):
                    sel_lines = [s]
                    while i < len(lines) and (sel_lines[-1].endswith(",") or lines[i].strip().startswith(('"', "`"))):
                        sel_lines.append(lines[i].strip())
                        i += 1
                        if not sel_lines[-1].endswith(","):
                            break
                    full = " ".join(sel_lines)
                    choices = [
                        (c1 or c2, cl.lower())
                        for c1, c2, cl in re.findall(r'(?:"([^"]+)"|`([^`]+)`)\s*,\s*\*([a-zA-Z0-9_]+)', full)
                    ]
                    self.all_menus[lbl] = choices
                    for _, cl in choices:
                        f_edges[lbl].append(cl)

        rev = defaultdict(set)
        for u, tgts in f_edges.items():
            for v in tgts:
                rev[v].add(u)

        can_reach_ending = set(good_end_fs)
        q = deque(good_end_fs)
        while q:
            u = q.popleft()
            for p in rev[u]:
                if p not in can_reach_ending:
                    can_reach_ending.add(p)
                    q.append(p)

        for f, choices in self.all_menus.items():
            if any(t == "endofplay" for _, t in choices):
                continue
            has_safe = any(t in can_reach_ending for _, t in choices)
            if not has_safe:
                continue
            for idx, (_, t) in enumerate(choices):
                if t not in can_reach_ending:
                    self.bad_end_menu_indices[(f, idx)] = True

        print(f"[2/4] Computed {len(self.bad_end_menu_indices)} exact Bad-End choice traps across {len(self.all_menus)} menus.")

    def _track_var(self, raw_var):
        v = map_var(raw_var)
        if not v.startswith("persistent."):
            self.local_variables.add(v)
        return v

    def _transpile_condition(self, raw_cond):
        """Translate NScripter boolean condition to Python, respecting unlock_all_routes."""
        c = raw_cond.strip()
        # Canonical progression gate patterns
        if re.fullmatch(r"%clear_ark\s*==\s*0\s*&&\s*%clear_ciel\s*==\s*0", c):
            return "not can_enter_far_side()"
        if re.fullmatch(r"%clear_hisui\s*!=\s*0", c):
            return "can_enter_hisui_unlocked()"
        if re.fullmatch(r"%cleared\s*!=\s*0", c):
            return "can_enter_cleared_branch()"
        if re.fullmatch(r"%ark_normalcleared\s*!=\s*0", c):
            return "can_enter_ark_good()"
        if re.fullmatch(r"%kohaku_regard\s*>\s*%hisui_regard\s*&&\s*%clear_hisui\s*!=\s*0", c):
            self._track_var("kohaku_regard")
            self._track_var("hisui_regard")
            return "(kohaku_regard > hisui_regard and can_enter_kohaku())"

        # General condition conversion
        cond_py = re.sub(r"%([a-zA-Z0-9_]+)", lambda m: self._track_var(m.group(1)), c)
        cond_py = re.sub(r"(?<![<>=!])=(?!=)", "==", cond_py)
        cond_py = re.sub(r"&&", " and ", cond_py)
        cond_py = re.sub(r"\|\|", " or ", cond_py)
        return cond_py

    def transpile_block(self, lbl, lines):
        out = [f"label {lbl}:\n"]

        # Clean endofplay: reset single-run vars and return cleanly to Main Menu (NO infinite loop!)
        if lbl == "endofplay":
            out.append("    $ quick_menu = False\n")
            out.append("    nvl clear\n")
            out.append("    stop music fadeout 1.5\n")
            out.append("    stop ambient fadeout 1.0\n")
            out.append("    stop sound\n")
            out.append("    $ current_fc_node_id = None\n")
            out.append("    $ tsuki_reset_run_state()\n")
            out.append("    $ tsuki_solid('#000000', 'crossfade_mid')\n")
            out.append("    $ renpy.pause(0.6)\n")
            out.append("    $ renpy.set_return_stack([])\n")
            out.append("    return\n\n")
            return "".join(out)

        chunk_buf = []
        current_text_color = None
        quote_depth = 0
        nvl_lines_on_page = 0
        page_has_text = False
        pending_br_count = 0
        s65_heartbeat_count = 0
        s65_saw_ark_e01 = False

        CLICKSTR_CHARS = ("。", "！", "？", "」", "』")
        apply_zh_hans_fixes = (self.edition_lang == "zh_hans")
        chars_per_line = 70 if self.edition_lang == "en" else 34

        def clear_nvl():
            nonlocal nvl_lines_on_page, page_has_text, pending_br_count, quote_depth
            if page_has_text:
                out.append("    nvl clear\n")
                page_has_text = False
            nvl_lines_on_page = 0
            pending_br_count = 0
            quote_depth = 0

        def format_styled_lines(cleaned_lines):
            nonlocal quote_depth
            styled = []
            for ln_txt in cleaned_lines:
                if ln_txt == "":
                    styled.append("")
                    continue
                esc = convert_inline_nscripter_tags(escape_renpy_text(ln_txt))
                starts_q = ln_txt.startswith(("「", "『"))
                is_q = starts_q or (quote_depth > 0)
                opens = ln_txt.count("「") + ln_txt.count("『")
                closes = ln_txt.count("」") + ln_txt.count("』")
                quote_depth = max(0, quote_depth + opens - closes)
                if current_text_color == "#ff0000":
                    styled.append(f"{{color=#ff5c6c}}{esc}{{/color}}")
                elif current_text_color == "#0000ff":
                    styled.append(f"{{color=#5cc8ff}}{esc}{{/color}}")
                elif is_q:
                    styled.append(f"{{color=#ffffff}}{esc}{{/color}}")
                else:
                    styled.append(esc)
            return "\\n".join(styled)

        def flush_chunk(clear_after=False):
            nonlocal chunk_buf, nvl_lines_on_page, page_has_text, pending_br_count
            if chunk_buf:
                cleaned_lines = []
                for subl in chunk_buf:
                    if subl == "":
                        cleaned_lines.append("")
                    else:
                        has_indent = subl.startswith("\u3000")
                        csub = sanitize_text(subl, apply_zh_fixes=apply_zh_hans_fixes)
                        if csub:
                            if has_indent and not csub.startswith(("「", "『", "—", "…")):
                                cleaned_lines.append("\u3000" + csub)
                            else:
                                cleaned_lines.append(csub)
                chunk_buf = []

                while cleaned_lines and cleaned_lines[0] == "":
                    cleaned_lines.pop(0)
                    pending_br_count += 1
                while cleaned_lines and cleaned_lines[-1] == "":
                    cleaned_lines.pop()

                if cleaned_lines:
                    raw_plain = "\n".join(cleaned_lines)
                    vis_lines = estimate_visual_lines(raw_plain, chars_per_line=chars_per_line)
                    extra_lines = min(pending_br_count, 6)
                    if page_has_text and (nvl_lines_on_page + vis_lines + extra_lines > 13):
                        out.append("    nvl clear\n")
                        nvl_lines_on_page = 0
                        page_has_text = False
                        extra_lines = min(pending_br_count, 6)

                    # Preserve dramatic vertical isolation (e.g. multiple `br` centering a line)
                    prefix = ""
                    if extra_lines > 0:
                        if page_has_text:
                            prefix = f"{{vspace={extra_lines * 28}}}"
                        elif extra_lines >= 3:
                            prefix = f"{{vspace={extra_lines * 42}}}"
                    pending_br_count = 0

                    formatted = format_styled_lines(cleaned_lines)
                    out.append(f'    n "{prefix}{formatted}"\n')

                    nvl_lines_on_page += vis_lines + extra_lines + 0.35
                    page_has_text = True

            if clear_after:
                clear_nvl()

        i = 0
        n_lines = len(lines)

        while i < n_lines:
            line = lines[i]
            sline = line.strip()
            i += 1

            if not sline or sline.startswith(";"):
                continue

            # Standalone page-clear `\` or click-wait `@` (preserves visual-only click pauses like ed_17 & cel_f01b!)
            if sline == "\\":
                if chunk_buf or page_has_text:
                    flush_chunk(clear_after=True)
                else:
                    out.append("    pause\n")
                continue

            if sline == "@":
                if chunk_buf or page_has_text:
                    flush_chunk(clear_after=False)
                else:
                    out.append("    pause\n")
                continue

            first_token = sline.split()[0].split(",")[0].lower()

            # Ignore pure legacy engine commands
            if first_token in ENGINE_COMMANDS_TO_IGNORE:
                continue

            # Text color toggles
            if sline.lower() in ("#ffffff", "#ff0000", "#0000ff"):
                flush_chunk(clear_after=False)
                current_text_color = None if sline.lower() == "#ffffff" else sline.lower()
                continue

            # Handle special `if %flgE>=1 skip N` Day-6 Arcueid/Ciel phase card branch
            if re.match(r"^if\s+%flgE\s*>=\s*1\s+skip\s+\d+", sline):
                flush_chunk(clear_after=True)
                self._track_var("flgE")
                # Consume both branches cleanly up through the second `gosub *left_phase`
                branch_a = []
                branch_b = []
                in_b = False
                while i < n_lines:
                    nxt = lines[i].strip()
                    i += 1
                    if not nxt or nxt.startswith(";"):
                        continue
                    if nxt.startswith("skip "):
                        in_b = True
                        continue
                    if not in_b:
                        branch_a.append(nxt)
                    else:
                        branch_b.append(nxt)
                        if nxt.startswith("gosub *left_phase") or nxt.startswith("gosub *right_phase"):
                            break

                def emit_phase_branch(blist, ind):
                    for bl in blist:
                        if bl.startswith("mov $phasebg"):
                            m = re.search(r'image\\(bg|event)\\([^"]+)', bl)
                            if m:
                                out.append(f'{ind}$ phase_bg = "{os.path.splitext(m.group(2))[0]}"\n')
                        elif bl.startswith("mov $phasetitle_a"):
                            m = re.search(r'image\\word\\([^"]+)', bl)
                            if m:
                                out.append(f'{ind}$ phase_title_a = "{os.path.splitext(m.group(1))[0]}"\n')
                        elif bl.startswith("mov $phasetitle_b"):
                            m = re.search(r'image\\word\\([^"]+)', bl)
                            if m:
                                out.append(f'{ind}$ phase_title_b = "{os.path.splitext(m.group(1))[0]}"\n')
                        elif bl.startswith("gosub *left_phase"):
                            out.append(f"{ind}call tsuki_left_phase\n")
                        elif bl.startswith("gosub *right_phase"):
                            out.append(f"{ind}call tsuki_right_phase\n")

                out.append("    if flgE >= 1:\n")
                emit_phase_branch(branch_b, "        ")
                out.append("    else:\n")
                emit_phase_branch(branch_a, "        ")
                continue

            # Handle `mov %flushcount, 0` flash loop (s180 & s289a)
            if sline.startswith("mov %flushcount"):
                flush_chunk(clear_after=False)
                flash_col = "#ffffff"
                restore_bg = None
                while i < n_lines:
                    nxt = lines[i].strip()
                    i += 1
                    if nxt.startswith("bg #"):
                        flash_col = nxt.split()[1].split(",")[0]
                    elif nxt.startswith('bg "image\\bg\\'):
                        m = re.search(r'image\\bg\\([^"]+)', nxt)
                        if m:
                            restore_bg = os.path.splitext(m.group(1))[0]
                    elif "skip -" in nxt:
                        break
                out.append(f'    $ tsuki_flash("{flash_col}")\n')
                if restore_bg:
                    out.append(f'    $ tsuki_bg("{restore_bg}", "nowaitdisp")\n')
                out.append("    with vpunch\n")
                continue

            # Ignore stray `skip N` (if any left)
            if first_token == "skip":
                continue

            # Phase title variables (3-layer authentic chapter title cards!)
            if sline.startswith("mov $phasebg"):
                m = re.search(r'image\\(bg|event)\\([^"]+)', sline)
                if m:
                    flush_chunk(clear_after=True)
                    folder, fn = m.groups()
                    bname = os.path.splitext(fn)[0]
                    out.append(f'    $ phase_bg = "{bname}"\n')
                    out.append(f'    $ phase_bg_kind = "{"cg" if folder == "event" else "bg"}"\n')
                continue

            if sline.startswith("mov $phasetitle_a"):
                m = re.search(r'image\\word\\([^"]+)', sline)
                if m:
                    flush_chunk(clear_after=True)
                    out.append(f'    $ phase_title_a = "{os.path.splitext(m.group(1))[0]}"\n')
                else:
                    out.append('    $ phase_title_a = ""\n')
                continue

            if sline.startswith("mov $phasetitle_b"):
                m = re.search(r'image\\word\\([^"]+)', sline)
                if m:
                    flush_chunk(clear_after=True)
                    out.append(f'    $ phase_title_b = "{os.path.splitext(m.group(1))[0]}"\n')
                else:
                    out.append('    $ phase_title_b = ""\n')
                continue

            # Background / CG / Full-RGB Word / Solid Fill
            if sline.startswith("bg "):
                flush_chunk(clear_after=True)
                m = re.search(r'bg\s+(?:(?:"image\\(bg|event|word)\\([^"]+)")|(#\w+))(?:\s*,\s*(.+))?', sline)
                if m:
                    folder, fname, color, raw_tr = m.groups()
                    tr = normalize_transition(raw_tr)
                    if color:
                        out.append(f'    $ tsuki_solid("{color.lower()}", "{tr}")\n')
                    elif folder == "bg":
                        bname = os.path.splitext(fname)[0]
                        # Optional subtle cinematic beats (gated by persistent.enable_cinematic_motion in runtime)
                        if lbl == "s20" and bname == "cmo_03":
                            out.append('    $ tsuki_play_se("se_02")\n')
                            out.append("    with hpunch\n")
                            out.append('    $ tsuki_bg("ima_11", "flash_white")\n')
                            out.append(f'    $ tsuki_bg("{bname}", "{tr}")\n')
                        elif lbl == "s65" and bname in ("ima_11b", "ima_13"):
                            out.append(f'    $ tsuki_bg("{bname}", "flash_red")\n')
                            out.append("    with vpunch\n")
                        else:
                            out.append(f'    $ tsuki_bg("{bname}", "{tr}")\n')
                    elif folder == "event":
                        cname = os.path.splitext(fname)[0]
                        out.append(f'    $ tsuki_cg("{cname}", "{tr}")\n')
                        if cname == "ark_e01" and lbl == "s65":
                            s65_saw_ark_e01 = True
                            out.append("    with vpunch\n")
                    elif folder == "word":
                        wname = os.path.splitext(fname)[0]
                        out.append(f'    $ tsuki_word_bg("{wname}", "{tr}")\n')
                continue

            # Monochrome mode (true scene-layer MatrixColor)
            if sline.startswith("monocro"):
                flush_chunk(clear_after=False)
                parts = sline.split()
                if len(parts) > 1 and parts[1].lower() != "off":
                    out.append(f'    $ tsuki_monocro("{parts[1].lower()}")\n')
                else:
                    out.append("    $ tsuki_monocro(None)\n")
                continue

            # Character Standing Sprite (3-slot dynamic engine!)
            if sline.startswith("ld "):
                flush_chunk(clear_after=False)
                m = re.search(r'ld\s+([lcr]),\s*":a;image\\tachi\\([^"]+)"(?:\s*,\s*(.+))?', sline)
                if m:
                    slot, fname, raw_tr = m.groups()
                    tname = os.path.splitext(fname)[0]
                    tr = normalize_transition(raw_tr)
                    out.append(f'    $ tsuki_ld("{slot}", "{tname}", "{tr}")\n')
                continue

            # Clear Standing Sprite (3-slot dynamic engine!)
            if sline.startswith("cl "):
                flush_chunk(clear_after=False)
                m = re.search(r"cl\s+([lcra])(?:\s*,\s*(.+))?", sline)
                if m:
                    slot, raw_tr = m.groups()
                    tr = normalize_transition(raw_tr)
                    out.append(f'    $ tsuki_cl("{slot}", "{tr}")\n')
                continue

            # Scene-skip wrapper in *f labels (keep inner gosub *sXX and mov %var, 1)
            if sline.startswith("if %sceneskip"):
                flush_chunk(clear_after=True)
                while i < n_lines:
                    nxt = lines[i].strip()
                    i += 1
                    if nxt.startswith("gosub *s"):
                        target_s = nxt.split("*")[-1].strip().split()[0].lower()
                        out.append(f"    call {target_s}\n")
                    elif nxt.startswith("mov %"):
                        m_mov = re.search(r"mov\s+%([a-zA-Z0-9_]+)\s*,\s*([0-9]+)", nxt)
                        if m_mov:
                            v = self._track_var(m_mov.group(1))
                            out.append(f"    $ {v} = {m_mov.group(2)}\n")
                    elif nxt.startswith("*skip"):
                        while i < n_lines and (lines[i].strip() in ("return", "") or lines[i].strip().startswith(";gosub")):
                            i += 1
                        break
                continue

            if sline.startswith("*skip"):
                while i < n_lines and (lines[i].strip() in ("return", "") or lines[i].strip().startswith(";gosub")):
                    i += 1
                continue

            # User Selection Menus
            if sline.startswith("select ") or sline.startswith("select\t"):
                flush_chunk(clear_after=True)
                sel_lines = [sline]
                while i < n_lines and (sel_lines[-1].endswith(",") or lines[i].strip().startswith(('"', "`"))):
                    sel_lines.append(lines[i].strip())
                    i += 1
                    if not sel_lines[-1].endswith(","):
                        break
                full_select_str = " ".join(sel_lines)
                choices = [
                    (c1 or c2, cl)
                    for c1, c2, cl in re.findall(r'(?:"([^"]+)"|`([^`]+)`)\s*,\s*\*([a-zA-Z0-9_]+)', full_select_str)
                ]
                if choices:
                    out.append(f'    $ _current_menu_id = "{lbl}"\n')
                    out.append("    menu:\n")
                    for ctext, clbl in choices:
                        cleaned_ctext = escape_renpy_text(sanitize_text(ctext, apply_zh_fixes=apply_zh_hans_fixes))
                        target_lbl = clbl.strip().lower()
                        out.append(f'        "{cleaned_ctext}":\n')
                        out.append(f"            jump {target_lbl}\n")
                continue

            # Conditional Jumps
            if sline.startswith("if "):
                flush_chunk(clear_after=False)
                m_goto = re.search(r"if\s+(.+)\s+goto\s+\*([a-zA-Z0-9_]+)", sline)
                if m_goto:
                    cond_py = self._transpile_condition(m_goto.group(1))
                    tgt = m_goto.group(2).strip().lower()
                    out.append(f"    if {cond_py}:\n")
                    out.append(f"        jump {tgt}\n")
                continue

            # Unconditional Jumps
            if sline.startswith("goto "):
                flush_chunk(clear_after=True)
                tgt = sline.split("*")[-1].strip().split()[0].lower()
                if tgt in ("title", "title2", "title_tochu"):
                    out.append("    return\n")
                else:
                    out.append(f"    jump {tgt}\n")
                continue

            # Subroutine Calls
            if sline.startswith("gosub "):
                flush_chunk(clear_after=True)
                tgt = sline.split("*")[-1].strip().split()[0].lower()
                if tgt == "regard_update":
                    continue
                if tgt in ("left_phase", "right_phase", "center_phase"):
                    out.append(f"    call tsuki_{tgt}\n")
                else:
                    out.append(f"    call {tgt}\n")
                continue

            # Returns
            if sline == "return":
                flush_chunk(clear_after=True)
                out.append("    return\n")
                continue

            # Variable Arithmetic Operations
            if sline.startswith("mov "):
                m = re.search(r"mov\s+%([a-zA-Z0-9_]+)\s*,\s*([0-9]+)", sline)
                if m:
                    var = self._track_var(m.group(1))
                    out.append(f"    $ {var} = {m.group(2)}\n")
                continue

            if sline.startswith("inc "):
                m = re.search(r"inc\s+%([a-zA-Z0-9_]+)", sline)
                if m:
                    var = self._track_var(m.group(1))
                    out.append(f"    $ {var} += 1\n")
                continue

            if sline.startswith("dec "):
                m = re.search(r"dec\s+%([a-zA-Z0-9_]+)", sline)
                if m:
                    var = self._track_var(m.group(1))
                    out.append(f"    $ {var} -= 1\n")
                continue

            if sline.startswith("add "):
                m = re.search(r"add\s+%([a-zA-Z0-9_]+)\s*,\s*([0-9]+)", sline)
                if m:
                    var = self._track_var(m.group(1))
                    out.append(f"    $ {var} += {m.group(2)}\n")
                continue

            if sline.startswith("sub "):
                m = re.search(r"sub\s+%([a-zA-Z0-9_]+)\s*,\s*([0-9]+)", sline)
                if m:
                    var = self._track_var(m.group(1))
                    out.append(f"    $ {var} -= {m.group(2)}\n")
                continue

            # Audio - Music & CD Play (safe runtime lookup across WAV/FLAC/OGG/MP3 & optional BGM)
            if sline.startswith(("mp3loop ", "mp3 ", "play ")):
                flush_chunk(clear_after=False)
                track = sline.split(None, 1)[1].strip()
                audio_stem = resolve_audio_stem(track)
                out.append(f'    $ tsuki_play_bgm("{audio_stem}")\n')
                continue

            if sline in ("stop", "playstop"):
                flush_chunk(clear_after=False)
                out.append("    stop music fadeout 1.2\n")
                continue

            # Audio - One-shot & Looping Sound Effects
            if sline.startswith("waveloop "):
                flush_chunk(clear_after=False)
                m = re.search(r'waveloop\s+(?:(?:"([^"]+)")|(\w+))', sline)
                if m:
                    audio_stem = resolve_audio_stem(m.group(1) or m.group(2))
                    out.append(f'    $ tsuki_play_ambient("{audio_stem}")\n')
                continue

            if sline.startswith("wave "):
                flush_chunk(clear_after=False)
                m = re.search(r'wave\s+(?:(?:"([^"]+)")|(\w+))', sline)
                if m:
                    target = m.group(1) or m.group(2)
                    audio_stem = resolve_audio_stem(target)
                    out.append(f'    $ tsuki_play_se("{audio_stem}")\n')
                    if lbl == "s65" and s65_saw_ark_e01 and target.lower() in ("se0", "se_01.wav", "se_01"):
                        s65_heartbeat_count += 1
                        if s65_heartbeat_count <= 4:
                            out.append('    $ tsuki_cinematic_pulse("red")\n')
                continue

            if sline == "wavestop":
                flush_chunk(clear_after=False)
                out.append("    stop sound\n")
                out.append("    stop ambient fadeout 0.5\n")
                continue

            # Pauses & Delays (properly resolves %staffrollwait = 4000ms!)
            if sline.startswith("!w") or sline.startswith("waittimer") or sline.startswith("delay"):
                flush_chunk(clear_after=False)
                if sline.startswith("!w"):
                    try:
                        ms = int(sline[2:])
                    except ValueError:
                        ms = 1000
                    out.append(f"    $ renpy.pause({round(ms / 1000.0, 2)})\n")
                else:
                    parts = sline.split()
                    arg = parts[1] if len(parts) > 1 else "1000"
                    if arg.startswith("%"):
                        v = self._track_var(arg[1:])
                        out.append(f"    $ renpy.pause(max(0.1, {v} / 1000.0))\n")
                    else:
                        try:
                            ms = int(arg)
                        except ValueError:
                            ms = 1000
                        out.append(f"    $ renpy.pause({round(ms / 1000.0, 2)})\n")
                continue

            # Screen Shakes
            if sline.startswith("quakey"):
                flush_chunk(clear_after=False)
                out.append("    with vpunch\n")
                continue

            if sline.startswith("quakex"):
                flush_chunk(clear_after=False)
                out.append("    with hpunch\n")
                continue

            # Line Break (`br`)
            if sline == "br":
                if chunk_buf:
                    chunk_buf.append("")
                else:
                    pending_br_count += 1
                continue

            # Regular NVL Story Text (respects NScripter `clickstr "」。！？", 2` + `\` + `@` + ONScripter EN backticks)
            ends_page = sline.endswith("\\")
            ends_wait = sline.endswith("@")
            body_raw = line.lstrip(" \t").rstrip()
            if ends_page or ends_wait:
                body_raw = body_raw[:-1]
            while body_raw.endswith("\\") or body_raw.endswith("@"):
                if body_raw.endswith("\\"):
                    ends_page = True
                else:
                    ends_wait = True
                body_raw = body_raw[:-1]

            if self.edition_lang == "en":
                # ONScripter English scripts wrap half-width text in backticks (`...`)
                body_raw = body_raw.replace("`", "")

            stripped_body = body_raw.strip()
            if stripped_body:
                chunk_buf.append(body_raw)
                # NScripter clickstr rule: check sentence-end punctuation AFTER stripping trailing inline `!w`/`!d`/`!s`
                click_check = re.sub(r"(?:![wd]\d+|!s(?:\d+|d))+$", "", stripped_body, flags=re.IGNORECASE).rstrip()
                if not ends_page and not ends_wait and self.edition_lang != "en" and click_check and click_check[-1] in CLICKSTR_CHARS:
                    ends_wait = True

            if ends_page:
                flush_chunk(clear_after=True)
            elif ends_wait:
                flush_chunk(clear_after=False)

        flush_chunk(clear_after=False)
        out.append("\n")
        return "".join(out)

    def transpile_all(self):
        story_dir = os.path.join(self.out_game_dir, "story")
        core_dir = os.path.join(self.out_game_dir, "core")
        os.makedirs(story_dir, exist_ok=True)
        os.makedirs(core_dir, exist_ok=True)

        chunks = {
            "story_prologue.rpy": [],
            "story_day01_day03.rpy": [],
            "story_near_routes.rpy": [],
            "story_far_routes.rpy": [],
            "story_branches.rpy": [],
            "story_badends_and_dojos.rpy": [],
        }

        emitted = 0
        for lbl in self.label_order:
            if lbl in DEAD_SYSTEM_LABELS:
                continue
            emitted += 1
            if lbl in ("openning", "ending", "s20", "eclipse"):
                chunks["story_prologue.rpy"].append(lbl)
            elif lbl.startswith("f"):
                chunks["story_branches.rpy"].append(lbl)
            elif lbl.startswith("s5") or lbl == "endofplay":
                chunks["story_badends_and_dojos.rpy"].append(lbl)
            else:
                m = re.search(r"\d+", lbl)
                num = int(m.group(0)) if m else 0
                if num <= 60:
                    chunks["story_day01_day03.rpy"].append(lbl)
                elif num <= 200:
                    chunks["story_near_routes.rpy"].append(lbl)
                else:
                    chunks["story_far_routes.rpy"].append(lbl)

        print(f"[3/4] Transpiling {emitted} active story labels into 6 NVL modules...")
        for fname, lbl_list in chunks.items():
            fpath = os.path.join(story_dir, fname)
            with open(fpath, "w", encoding="utf-8") as out_f:
                out_f.write("## ==========================================================================\n")
                out_f.write(f"## Tsukihime Classic HD NVL Story Module: {fname}\n")
                out_f.write(f"## Active labels: {len(lbl_list)}\n")
                out_f.write("## ==========================================================================\n\n")
                for lbl in lbl_list:
                    out_f.write(self.transpile_block(lbl, self.labels[lbl]))
            print(f"      [OK] {fname:30s}: {len(lbl_list):4d} labels")

        # Write local story variables + bad-end choice metadata into core/story_variables.rpy
        vars_path = os.path.join(core_dir, "story_variables.rpy")
        with open(vars_path, "w", encoding="utf-8") as vf:
            vf.write("## ==========================================================================\n")
            vf.write("## Single-Playthrough Story Variables & Bad-End Trap Metadata\n")
            vf.write("## (Cross-playthrough progression flags live in core/engine_state.rpy)\n")
            vf.write("## ==========================================================================\n\n")
            vf.write('default _current_menu_id = ""\n')
            vf.write('default phase_bg = ""\n')
            vf.write('default phase_bg_kind = "bg"\n')
            vf.write('default phase_title_a = ""\n')
            vf.write('default phase_title_b = ""\n')
            vf.write("default staffrollwait = 4000\n\n")
            for var in sorted(self.local_variables):
                if var in ("staffrollwait",):
                    continue
                vf.write(f"default {var} = 0\n")

            vf.write("\ninit -2 python:\n")
            vf.write("    # Mathematically derived Bad-End choice traps: (menu_label, 0-based choice index)\n")
            vf.write("    BAD_END_MENU_INDICES = {\n")
            for (flbl, idx) in sorted(self.bad_end_menu_indices.keys()):
                vf.write(f'        ("{flbl}", {idx}): True,\n')
            vf.write("    }\n\n")
            vf.write("    def tsuki_reset_run_state():\n")
            vf.write('        """Reset single-playthrough affection & route flags without touching persistent clears."""\n')
            vf.write("        for k in ('ark_regard', 'ciel_regard', 'akiha_regard', 'kohaku_regard', 'hisui_regard'):\n")
            vf.write("            setattr(store, k, 0)\n")
            vf.write("        for suffix in '123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ':\n")
            vf.write("            fn = 'flg' + suffix\n")
            vf.write("            if hasattr(store, fn):\n")
            vf.write("                setattr(store, fn, 0)\n")

        print(f"[4/4] Wrote {vars_path} ({len(self.local_variables)} local vars, {len(self.bad_end_menu_indices)} Bad-End traps).")
        print("=== Transpilation completed cleanly! ===")


def main():
    import argparse
    ap = argparse.ArgumentParser(description="Transpile NScripter Tsukihime script (0.txt / nscript.dat) to Ren'Py NVL.")
    ap.add_argument("--source", default="", help="Path to 0.txt or nscript.dat")
    ap.add_argument("--out", default=OUT_GAME, help="Target Ren'Py game/ directory")
    args = ap.parse_args()
    src = args.source or (SRC_0TXT if os.path.exists(SRC_0TXT) else FALLBACK_0TXT)
    if not os.path.exists(src):
        print(f"[ERROR] Source script not found at {src}")
        sys.exit(1)
    t = TsukihimeASTTranspiler(script_path=src, out_game_dir=args.out)
    t.transpile_all()


if __name__ == "__main__":
    main()
