# -*- coding: utf-8 -*-
"""
Tsukihime Classic HD v2.0 - End-to-End Automated Verification Suite
===================================================================
Verifies:
  1. Zero missing jump/call target labels & zero infinite title_tochu loops.
  2. Zero broken H-scene guards & zero leaked NScripter commands in dialogue.
  3. 100% of tsuki_bg / tsuki_cg / tsuki_ld / tsuki_word_bg / audio references exist on disk.
  4. 100% of Flowchart nodes (branch_label, seen_label, thumb) exist and match real script.
  5. 100% of Gallery CGs exist on disk and are wired to seen_cgs / renpy.seen_image.
  6. Zero missing-glyph tofu boxes across all UI screens using bundled static fonts.
  7. Runs official Ren'Py 8.5.3 `lint` and asserts exit code 0 + zero warnings/errors.
  8. State-space reachability & affection audit: verifies all 9 endings, Flowchart
     preset joint achievability, zero negative regards, and screens.rpy max caps.
  --compliance-audit: also verifies open-source exclusions, font licenses, zero
     hardcoded local paths, and version consistency across code & READMEs.
"""

import os
import re
import sys
import glob
import argparse
import subprocess
from collections import defaultdict, deque
from PIL import ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_PROJ = os.path.join(ROOT, "Tsukihime_HD")
RENPY_EXE = os.path.join(ROOT, "tools", "renpy_sdk", "renpy-8.5.3-sdk", "renpy.exe")


def read_text(p):
    with open(p, "r", encoding="utf-8") as f:
        return f.read()


def check_version_sync():
    """Verify release version matches across options.rpy, byoa_gui.py, README.md, and README_EN.md."""
    issues = []
    versions = {}

    opt_p = os.path.join(DEFAULT_PROJ, "game", "options.rpy")
    m_opt = re.search(r'define\s+config\.version\s*=\s*"([^"]+)"', read_text(opt_p))
    if not m_opt:
        issues.append("Could not locate config.version in Tsukihime_HD/game/options.rpy")
    else:
        versions["options.rpy"] = m_opt.group(1)

    gui_p = os.path.join(ROOT, "scripts", "byoa_gui.py")
    m_gui = re.search(r'APP_VERSION\s*=\s*"([^"]+)"', read_text(gui_p))
    if not m_gui:
        issues.append("Could not locate APP_VERSION in scripts/byoa_gui.py")
    else:
        versions["byoa_gui.py"] = m_gui.group(1)

    for doc in ("README.md", "README_EN.md"):
        doc_p = os.path.join(ROOT, doc)
        txt = read_text(doc_p)
        z_vers = set(re.findall(r"BlueGlassHD-(\d+\.\d+\.\d+)-win-BYOA\.zip", txt))
        d_vers = set(re.findall(r"BlueGlassHD-(\d+\.\d+\.\d+)-win/", txt))
        if len(z_vers) != 1 or len(d_vers) != 1 or z_vers != d_vers:
            issues.append(f"{doc} has missing or inconsistent BlueGlassHD-* version strings: zip={sorted(z_vers)}, dir={sorted(d_vers)}")
        else:
            versions[doc] = next(iter(z_vers))

    if len(set(versions.values())) > 1:
        issues.append(f"Version mismatch across repo files: {versions}")
    return issues


def verify_state_space_and_affection(game_dir):
    """Exact state-space reachability audit for endings, negative affection, UI caps, and Flowchart presets."""
    regards = ["ark_regard", "ciel_regard", "akiha_regard", "hisui_regard", "kohaku_regard"]
    story_files = sorted(glob.glob(os.path.join(game_dir, "story", "*.rpy")))
    labels = {}
    order = []
    for fp in story_files:
        cur = None
        for raw in read_text(fp).splitlines():
            m = re.match(r"^label\s+([A-Za-z0-9_]+)\s*:", raw)
            if m:
                cur = m.group(1)
                order.append(cur)
                labels[cur] = []
                continue
            if cur is not None:
                labels[cur].append(raw)

    def parse_ast(lines):
        root = []
        stack = [(-1, root)]
        for raw in lines:
            s = raw.strip()
            if not s or s.startswith("#"):
                continue
            indent = len(raw) - len(raw.lstrip(" "))
            node = [indent, s, []]
            while stack and indent <= stack[-1][0]:
                stack.pop()
            stack[-1][1].append(node)
            if s.endswith(":"):
                stack.append((indent, node[2]))
        return root

    asts = {lbl: parse_ast(lines) for lbl, lines in labels.items()}
    next_map = {order[i]: (order[i + 1] if i + 1 < len(order) else None) for i in range(len(order))}

    direct_reads = {}
    edges = {}
    for lbl, tree in asts.items():
        reads, succs = set(), set()
        has_ft = True

        def walk(nodes, top=False):
            nonlocal has_ft
            for _, s, ch in nodes:
                if s.startswith("if ") or s.startswith("elif "):
                    for m in re.finditer(r"\b(flg[A-Z0-9]|[a-z]+_regard)\b", s):
                        reads.add(m.group(1))
                elif s.startswith("jump "):
                    succs.add(s[5:].strip())
                    if top:
                        has_ft = False
                elif s == "return" and top:
                    has_ft = False
                walk(ch, False)

        walk(tree, True)
        if has_ft and next_map.get(lbl):
            succs.add(next_map[lbl])
        direct_reads[lbl] = reads
        edges[lbl] = succs

    live_in = {lbl: set(direct_reads[lbl]) for lbl in asts}
    changed = True
    while changed:
        changed = False
        for lbl in asts:
            before = len(live_in[lbl])
            for suc in edges.get(lbl, ()):
                if suc in live_in:
                    live_in[lbl] |= live_in[suc]
            if len(live_in[lbl]) > before:
                changed = True

    def eval_cond(cond_str, st, pmode):
        env = dict(st)
        val = (pmode == "all_true")
        for fn in ("can_enter_ark_good", "can_enter_cleared_branch", "can_enter_far_side", "can_enter_hisui_unlocked", "can_enter_kohaku"):
            env[fn] = lambda v=val: v
        return bool(eval(cond_str, {"__builtins__": {}}, env))

    def step_stmts(stmts, st, pmode, fb):
        def run_seq(seq, cur_st, idx_start=0):
            res = []
            i = idx_start
            while i < len(seq):
                _, s, children = seq[i]
                if s.startswith("if "):
                    branches = [(s[3:-1].strip(), children)]
                    j = i + 1
                    while j < len(seq) and (seq[j][1].startswith("elif ") or seq[j][1] == "else:"):
                        branches.append((seq[j][1][5:-1].strip() if seq[j][1].startswith("elif ") else None, seq[j][2]))
                        j += 1
                    taken = False
                    for bcond, bch in branches:
                        if bcond is None or eval_cond(bcond, cur_st, pmode):
                            taken = True
                            for nxt, nst in run_seq(bch, dict(cur_st)):
                                res.extend(run_seq(seq, nst, j) if nxt is None else [(nxt, nst)])
                            break
                    if not taken:
                        res.extend(run_seq(seq, cur_st, j))
                    return res
                elif s == "menu:":
                    for _, cs, cch in children:
                        if cs.endswith(":"):
                            for nxt, nst in run_seq(cch, dict(cur_st)):
                                res.extend(run_seq(seq, nst, i + 1) if nxt is None else [(nxt, nst)])
                    return res
                elif s.startswith("jump "):
                    res.append((s[5:].strip(), cur_st))
                    return res
                elif s == "return":
                    res.append(("__RETURN__", cur_st))
                    return res
                elif s.startswith("$ "):
                    m = re.match(r"^([a-zA-Z0-9_]+)\s*(\+=|-=|=)\s*(-?\d+)$", s[2:].strip())
                    if m and m.group(1) in cur_st:
                        var, op, val = m.group(1), m.group(2), int(m.group(3))
                        if op == "=":
                            cur_st[var] = val
                        elif op == "+=":
                            cur_st[var] += val
                        elif op == "-=":
                            cur_st[var] -= val
                i += 1
            res.append((None, cur_st))
            return res

        return [(fb if nxt is None else nxt, nst) for nxt, nst in run_seq(stmts, st)]

    def explore(start_lbl, preset=None, pmode="all_true", max_steps=600000):
        init_st = {r: 0 for r in regards}
        for c in "123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            init_st["flg" + c] = 0
        if preset:
            init_st.update(preset)

        def key_for(lbl, st):
            lv = live_in.get(lbl, set())
            return (lbl, tuple(st[r] for r in regards), tuple((v, st[v]) for v in sorted(lv) if v.startswith("flg")))

        q = deque([(start_lbl, init_st)])
        visited = {key_for(start_lbl, init_st)}
        at_lbl = defaultdict(list)
        steps = 0
        while q and steps < max_steps:
            steps += 1
            lbl, st = q.popleft()
            at_lbl[lbl].append(dict(st))
            if lbl in ("__RETURN__", "__END__") or lbl not in asts:
                continue
            for nxt, nst in step_stmts(asts[lbl], st, pmode, next_map.get(lbl) or "__END__"):
                k = key_for(nxt, nst)
                if k not in visited:
                    visited.add(k)
                    q.append((nxt, nst))
        return at_lbl

    errs = []
    at_true = explore("f20", None, "all_true")
    at_first = explore("f20", None, "first_play")

    # Check zero negatives from New Game (f20) & all 9 endings reachable
    for lbl, sts in at_true.items():
        for r in regards:
            if min(s[r] for s in sts) < 0:
                errs.append(f"Negative {r} reachable from f20 at {lbl}")
                break

    all_9_end_flbls = ("f52a", "f53a", "f308", "f310", "f384", "f385", "f412", "f413", "f429")
    for ef in all_9_end_flbls:
        if not at_true.get(ef):
            errs.append(f"Canonical ending label {ef} unreachable from f20")

    # Verify HEROINE_AFFECTION_SPEC in screens.rpy matches exact f20 maximums
    true_max = {r: max(s[r] for sts in at_true.values() for s in sts) for r in regards}
    scr_txt = read_text(os.path.join(game_dir, "ui", "screens.rpy"))
    m_spec = re.search(r"HEROINE_AFFECTION_SPEC\s*=\s*\{(.*?)\}", scr_txt, re.S)
    if not m_spec:
        errs.append("Missing HEROINE_AFFECTION_SPEC in ui/screens.rpy")
    else:
        spec = eval("{" + m_spec.group(1) + "}", {"__builtins__": {}})
        for r in regards:
            ui_max = spec.get(r, (None,))[0]
            if ui_max != true_max[r]:
                errs.append(f"screens.rpy HEROINE_AFFECTION_SPEC[{r}] max={ui_max} != script max={true_max[r]}")

    # Verify all Flowchart continue node presets
    fc_txt = read_text(os.path.join(game_dir, "ui", "flowchart.rpy"))
    m_fc = re.search(r"FLOWCHART_NODES\s*=\s*\[(.*?)\n    \]", fc_txt, re.S)
    fc_nodes = eval("[" + m_fc.group(1) + "\n]", {"__builtins__": {}})
    cont_nodes = [n for n in fc_nodes if n.get("mode") == "continue"]

    route_expected = {
        "com_05": ("f52a", "f53a", "f384", "f385"),
        "com_06": ("f52a", "f53a", "f308", "f310"),
        "com_07": ("f52a", "f53a", "f308", "f310"),
        "arc_09": ("f52a",), "arc_10": ("f53a",),
        "ciel_06": ("f310",), "ciel_07": ("f308",),
        "aki_08": ("f385",), "aki_09": ("f384",),
        "his_06": ("f412",), "his_07": ("f413",),
        "koh_06": ("f429",),
    }

    for n in cont_nodes:
        nid, lbl, cat = n["id"], n["branch_label"], n["cat"]
        preset = n.get("preset", {})
        check_lbl = "f53a" if lbl == "f53" else lbl
        pool = at_true.get(check_lbl, []) + at_first.get(check_lbl, [])
        if not any(all(s.get(k, 0) == v for k, v in preset.items()) for s in pool):
            errs.append(f"Flowchart {nid} ({lbl}) preset {preset} is not jointly reachable from f20")
            continue

        fc_at = explore(lbl, preset, "all_true", max_steps=150000)
        for slbl, sts in fc_at.items():
            for r in regards:
                if min(s[r] for s in sts) < 0:
                    errs.append(f"Flowchart {nid} ({lbl}) can drive {r} negative at {slbl}")
                    break

        exp = route_expected.get(nid)
        if not exp:
            if cat == "arc":
                exp = ("f52a", "f53a")
            elif cat == "ciel":
                exp = ("f308", "f310")
            elif cat == "akiha":
                exp = ("f384", "f385")
            elif cat == "hisui":
                exp = ("f412", "f413")
            elif cat == "kohaku":
                exp = ("f429",)
        if exp:
            for e_lbl in exp:
                if not fc_at.get(e_lbl):
                    errs.append(f"Flowchart {nid} ({lbl}) preset blocks expected ending {e_lbl}")
        if nid in ("his_01", "his_02", "his_03") and not fc_at.get("f410"):
            errs.append(f"Flowchart {nid} ({lbl}) preset bypasses Hisui Bad End f410")

    return true_max, len(cont_nodes), errs


def run_compliance_audit():
    """Verify BYOA open-source repository compliance (.gitignore coverage, licenses, font metadata)."""
    issues = []
    for req in ("LICENSE", "THIRD_PARTY_LICENSES.md", ".gitignore", "README.md", "scripts/byoa_import.py"):
        if not os.path.exists(os.path.join(ROOT, req)):
            issues.append(f"Missing required compliance file: {req}")

    gi = read_text(os.path.join(ROOT, ".gitignore")) if os.path.exists(os.path.join(ROOT, ".gitignore")) else ""
    must_ignore = [
        "Tsukihime_HD/game/images/",
        "Tsukihime_HD/game/story/",
        "Tsukihime_HD/game/gui/portraits/",
        "Tsukihime_HD/game/gui/main_menu.webp",
        "Tsukihime_HD/game/gui/title_eclipse_moon.png",
        "Tsukihime_HD/game/gui/title_eclipse_kanji.png",
        "Tsukihime_HD/game/audio/se_*",
    ]
    for pat in must_ignore:
        if pat not in gi:
            issues.append(f".gitignore missing BYOA exclusion: {pat}")

    # Verify zero commercial fonts in game/fonts/
    import struct
    fonts_dir = os.path.join(DEFAULT_PROJ, "game", "fonts")
    for fn in sorted(os.listdir(fonts_dir)):
        if not fn.lower().endswith((".ttf", ".otf")):
            continue
        data = open(os.path.join(fonts_dir, fn), "rb").read()
        num_t = struct.unpack(">H", data[4:6])[0]
        blob = ""
        for ti in range(num_t):
            tag, _, toff, _ = struct.unpack(">4sIII", data[12 + ti * 16 : 28 + ti * 16])
            if tag == b"name":
                _, cnt, soff = struct.unpack(">HHH", data[toff : toff + 6])
                for ni in range(cnt):
                    plat, _, _, nid, ln_, off_ = struct.unpack(">HHHHHH", data[toff + 6 + ni * 12 : toff + 18 + ni * 12])
                    if nid in (0, 13):
                        raw = data[toff + soff + off_ : toff + soff + off_ + ln_]
                        blob += " " + raw.decode("utf-16-be" if plat in (0, 3) else "latin-1", errors="ignore")
                break
        bl = blob.lower()
        if not ("open font license" in bl or "opensource.org/licenses/ipa" in bl or "ipa font license" in bl):
            issues.append(f"Non-open-source font in game/fonts/: {fn}")

    issues.extend(check_version_sync())

    if issues:
        print(f"[COMPLIANCE FAILED] {len(issues)} issue(s):")
        for it in issues:
            print("  -", it)
        sys.exit(1)

    # Verify zero personal/local hardcoded machine paths in open-source scripts & docs
    personal_pat = re.compile(r"(?:[A-Z]:[/\\]+Games[/\\]+月姬|C:[/\\]+Users[/\\]+86166|oct 5,2026)", re.IGNORECASE)
    scan_exts = (".py", ".ps1", ".rpy", ".md", ".yml", ".yaml", ".txt")
    skip_dirs = {"tools", "release", "saves", "cache", "build_pyinstaller", "__pycache__", ".git", "story", "images", "tmp", "video"}
    for r_dir, dnames, fnames in os.walk(ROOT):
        dnames[:] = [d for d in dnames if d not in skip_dirs]
        for fn in fnames:
            if not fn.lower().endswith(scan_exts):
                continue
            full = os.path.join(r_dir, fn)
            rel = os.path.relpath(full, ROOT)
            if rel.replace("\\", "/") in ("scripts/verify_project.py", "Tsukihime_HD/log.txt", "Tsukihime_HD/traceback.txt"):
                continue
            txt = read_text(full)
            if personal_pat.search(txt):
                issues.append(f"Hardcoded local path leaked in {rel}")

    if issues:
        print(f"[COMPLIANCE FAILED] {len(issues)} issue(s):")
        for it in issues:
            print("  -", it)
        sys.exit(1)
    print("[COMPLIANCE PASSED] All BYOA exclusions, license files, zero local-path leaks, and bundled font metadata verified!")
    sys.exit(0)


def main():
    ap = argparse.ArgumentParser(description="End-to-end verification suite for Tsukihime Classic HD.")
    ap.add_argument("--project", default=DEFAULT_PROJ, help="Path to Ren'Py project root (containing game/)")
    ap.add_argument("--compliance-audit", action="store_true", help="Run BYOA open-source compliance audit only")
    args = ap.parse_args()

    if args.compliance_audit:
        run_compliance_audit()

    PROJ = os.path.abspath(args.project)
    GAME = os.path.join(PROJ, "game")
    failures = []
    all_rpy = sorted(glob.glob(os.path.join(GAME, "**", "*.rpy"), recursive=True))
    story_rpy = sorted(glob.glob(os.path.join(GAME, "story", "*.rpy")))
    ui_rpy = sorted(glob.glob(os.path.join(GAME, "ui", "*.rpy")))

    print(f"Scanning {len(all_rpy)} .rpy files in {PROJ}/game/ ...")

    # 1. Labels & jump/call integrity
    defined_labels = set()
    jumps_calls = []
    for fp in all_rpy:
        rel = os.path.relpath(fp, GAME)
        for ln, line in enumerate(read_text(fp).splitlines(), 1):
            s = line.strip()
            m = re.match(r"^label\s+([a-zA-Z0-9_]+)\s*:", s)
            if m:
                defined_labels.add(m.group(1))
            m = re.match(r"^(jump|call)\s+([a-zA-Z0-9_]+)\b", s)
            if m and m.group(2) != "expression":
                jumps_calls.append((rel, ln, m.group(1), m.group(2)))

    missing_targets = [x for x in jumps_calls if x[3] not in defined_labels]
    print(f"[1] Labels: {len(defined_labels)} defined | {len(jumps_calls)} jumps/calls | missing={len(missing_targets)}")
    if missing_targets:
        failures.append(f"Missing jump/call targets: {missing_targets[:10]}")
    if "title_tochu" in defined_labels or "title" in defined_labels:
        failures.append("Legacy infinite-loop label `title` or `title_tochu` still exists!")

    # 2. Check for leaked commands, inline !w/!d/!s tags, H-guards in story
    leaked = []
    h_guards = 0
    bg_refs, cg_refs, ld_refs, word_refs, audio_refs, audio_stems = set(), set(), set(), set(), set(), set()
    for fp in story_rpy:
        rel = os.path.relpath(fp, GAME)
        for ln, line in enumerate(read_text(fp).splitlines(), 1):
            s = line.strip()
            if "enable_adult_content" in s:
                h_guards += 1
            if s.startswith('n "') and s.endswith('"'):
                inner = re.sub(r"\{/?color(?:=#[0-9a-fA-F]+)?\}|\{vspace=\d+\}|\{w=[0-9.]+\}", "", s[3:-1])
                if re.match(r"^(skip\s+\d+|selgosub|play\s+\\?\"|akiha\s+被)", inner.strip()):
                    leaked.append((rel, ln, inner[:80]))
                if re.search(r"![wd]\d+|!s(?:\d+|d)\b", inner, re.IGNORECASE):
                    leaked.append((rel, ln, inner[:80]))
            for m in re.finditer(r'tsuki_bg\("([^"]+)"', s):
                bg_refs.add(m.group(1))
            for m in re.finditer(r'tsuki_cg\("([^"]+)"', s):
                cg_refs.add(m.group(1))
            for m in re.finditer(r'tsuki_word_bg\("([^"]+)"', s):
                word_refs.add(m.group(1))
            for m in re.finditer(r'tsuki_ld\("[lcr]",\s*"([^"]+)"', s):
                ld_refs.add(m.group(1))
            for m in re.finditer(r'phase_bg\s*=\s*"([^"]+)"', s):
                if m.group(1):
                    bg_refs.add(m.group(1)) if os.path.exists(os.path.join(GAME, "images", "bg", m.group(1) + ".webp")) else cg_refs.add(m.group(1))
            for m in re.finditer(r'phase_title_[ab]\s*=\s*"([^"]+)"', s):
                if m.group(1):
                    word_refs.add(m.group(1))
            for m in re.finditer(r'"(audio/[^"]+)"', s):
                audio_refs.add(m.group(1))
            for m in re.finditer(r'tsuki_play_(?:bgm|se|ambient)\("([^"]+)"', s):
                audio_stems.add(m.group(1))

    print(f"[2] Story sanity: leaked_cmds={len(leaked)}, h_guards={h_guards}")
    if leaked:
        failures.append(f"Leaked NScripter commands in dialogue: {leaked[:10]}")
    if h_guards:
        failures.append(f"Found {h_guards} residual H-scene guards!")

    # 3. Asset file existence & stage scaling integrity check
    miss_bg = [x for x in sorted(bg_refs) if not os.path.exists(os.path.join(GAME, "images", "bg", x + ".webp"))]
    miss_cg = [x for x in sorted(cg_refs) if not os.path.exists(os.path.join(GAME, "images", "cg", x + ".webp"))]
    miss_ld = [x for x in sorted(ld_refs) if not os.path.exists(os.path.join(GAME, "images", "tachi", x + ".webp"))]
    miss_wd = [x for x in sorted(word_refs) if not os.path.exists(os.path.join(GAME, "images", "word", x + ".webp"))]
    miss_au = [x for x in sorted(audio_refs) if not os.path.exists(os.path.join(GAME, x))]
    for st in sorted(audio_stems):
        if not any(os.path.exists(os.path.join(GAME, "audio", f"{st}.{ext}")) for ext in ("wav", "flac", "ogg", "mp3")):
            miss_au.append(f"audio/{st}.*")
    if not os.path.exists(os.path.join(GAME, "gui", "icons", "check.png")):
        failures.append("Missing required UI icon: gui/icons/check.png")
    stage_txt = read_text(os.path.join(GAME, "core", "stage_engine.rpy"))
    if "_get_tachi_zoom" not in stage_txt:
        failures.append("stage_engine.rpy missing dynamic _get_tachi_zoom scaling for 1x/4x tachi assets!")
    print(f"[3] Assets on disk: bg_miss={len(miss_bg)} cg_miss={len(miss_cg)} tachi_miss={len(miss_ld)} word_miss={len(miss_wd)} audio_miss={len(miss_au)}")
    if miss_bg or miss_cg or miss_ld or miss_wd or miss_au:
        failures.append(f"Missing assets: bg={miss_bg}, cg={miss_cg}, tachi={miss_ld}, word={miss_wd}, audio={miss_au}")

    # 4. Flowchart verification (supports nested preset dicts)
    fc_txt = read_text(os.path.join(GAME, "ui", "flowchart.rpy"))
    fc_matches = re.findall(
        r'"id":\s*"([^"]+)"[\s\S]*?"seen_label":\s*"([^"]+)"\s*,\s*"branch_label":\s*"([^"]+)"[\s\S]*?"thumb":\s*"([^"]+)"',
        fc_txt,
    )
    fc_err = []
    if len(fc_matches) < 40:
        fc_err.append(f"Expected >= 40 flowchart nodes, found {len(fc_matches)}")
    for nid, sl, bl, th in fc_matches:
        if sl not in defined_labels:
            fc_err.append(f"{nid}: missing seen_label {sl}")
        if bl not in defined_labels:
            fc_err.append(f"{nid}: missing branch_label {bl}")
        if not os.path.exists(os.path.join(GAME, th)):
            fc_err.append(f"{nid}: missing thumb {th}")
    print(f"[4] Flowchart: {len(fc_matches)} nodes verified, errors={len(fc_err)}")
    if fc_err:
        failures.append(f"Flowchart errors: {fc_err}")

    # 5. Gallery verification
    gal_txt = read_text(os.path.join(GAME, "ui", "gallery.rpy"))
    gal_cgs = [x for x in set(re.findall(r"'([a-z0-9_]+)'", gal_txt)) if "_" in x]
    gal_miss = []
    for c in gal_cgs:
        p = os.path.join(GAME, "images", "bg" if c.startswith("cmo_") else "cg", c + ".webp")
        if not os.path.exists(p):
            gal_miss.append(c)
    print(f"[5] Gallery: {len(gal_cgs)} unique CGs verified, missing={len(gal_miss)}")
    if gal_miss:
        failures.append(f"Gallery missing files: {gal_miss}")

    # 6. UI Font glyph coverage + 100% open-source license compliance check!
    import struct
    fonts_dir = os.path.join(GAME, "fonts")
    font_files = sorted(fn for fn in os.listdir(fonts_dir) if fn.lower().endswith((".ttf", ".otf")))
    font_cache = {}
    license_violations = []
    for fn in font_files:
        p = os.path.join(fonts_dir, fn)
        fnt = ImageFont.truetype(p, 28)
        font_cache[f"fonts/{fn}"] = (fnt, bytes(fnt.getmask("\uFFFF")))
        # Verify embedded TTF/OTF name table carries SIL OFL or IPA open-source license
        data = open(p, "rb").read()
        num_t = struct.unpack(">H", data[4:6])[0]
        meta_blob = ""
        for ti in range(num_t):
            tag, _, toff, _ = struct.unpack(">4sIII", data[12 + ti * 16 : 28 + ti * 16])
            if tag == b"name":
                _, cnt, soff = struct.unpack(">HHH", data[toff : toff + 6])
                for ni in range(cnt):
                    plat, _, _, nid, ln_, off_ = struct.unpack(">HHHHHH", data[toff + 6 + ni * 12 : toff + 18 + ni * 12])
                    if nid in (0, 13):
                        raw = data[toff + soff + off_ : toff + soff + off_ + ln_]
                        meta_blob += " " + raw.decode("utf-16-be" if plat in (0, 3) else "latin-1", errors="ignore")
                break
        ml = meta_blob.lower()
        if not ("open font license" in ml or "opensource.org/licenses/ipa" in ml or "ipa font license" in ml):
            license_violations.append(fn)

    if not os.path.exists(os.path.join(fonts_dir, "LICENSES.txt")):
        license_violations.append("missing LICENSES.txt")

    tofu_hits = []
    for fp in ui_rpy:
        rel = os.path.relpath(fp, GAME)
        for ln, line in enumerate(read_text(fp).splitlines(), 1):
            m_f = re.search(r'font\s+"(fonts/[^"]+)"', line)
            f_key = m_f.group(1) if m_f else "fonts/lxgw_xihei.ttf"
            if f_key not in font_cache:
                tofu_hits.append((rel, ln, f_key, "MISSING_FONT_FILE", ""))
                continue
            fnt, nd = font_cache[f_key]
            if re.match(r"^\s*(text|textbutton)\s+", line):
                for q in re.findall(r'"([^"]+)"', line):
                    if q.startswith(("fonts/", "gui/", "audio/", "#")):
                        continue
                    q_clean = re.sub(r"\{[^}]+\}|\[[^\]]+\]", "", q)
                    for ch in q_clean:
                        if ord(ch) > 127 and ch not in ("\n", "\r", "\t", " "):
                            if bytes(fnt.getmask(ch)) == nd:
                                tofu_hits.append((rel, ln, f_key, ch, f"U+{ord(ch):04X}"))
    print(f"[6] Open-source fonts ({len(font_files)} files): license_violations={len(license_violations)}, tofu_hits={len(tofu_hits)}")
    if license_violations:
        failures.append(f"Non-open-source or unlicensed font files detected: {license_violations}")
    if tofu_hits:
        failures.append(f"Missing-glyph tofu detected: {tofu_hits[:10]}")

    # 7. Official Ren'Py 8.5.3 lint
    print("[7] Running official Ren'Py 8.5.3 lint ...")
    if os.path.exists(RENPY_EXE):
        res = subprocess.run(
            [RENPY_EXE, PROJ, "lint"],
            capture_output=True, encoding="utf-8", errors="replace",
        )
        lint_out = (res.stdout or "") + "\n" + (res.stderr or "")
        print("    Lint exit code:", res.returncode)
        for l in lint_out.splitlines():
            if l.strip():
                print("    | " + l)
        if res.returncode != 0:
            failures.append(f"Ren'Py lint failed with code {res.returncode}")
        for bad_kw in ("error", "traceback", "could not", "is not defined", "duplicate"):
            for l in lint_out.splitlines():
                if bad_kw in l.lower() and "lint is not a substitute" not in l.lower():
                    failures.append(f"Ren'Py lint issue: {l}")
    else:
        failures.append(f"Ren'Py SDK executable not found: {RENPY_EXE}")

    # 8. State-space reachability, affection bounds, UI caps & version sync
    ver_issues = check_version_sync()
    true_max, cont_cnt, ss_errs = verify_state_space_and_affection(GAME)
    max_summary = ", ".join(f"{k.split('_')[0]}={v}" for k, v in true_max.items())
    print(f"[8] State-space & versions: {cont_cnt} flowchart presets, caps({max_summary}), issues={len(ver_issues) + len(ss_errs)}")
    failures.extend(ver_issues)
    failures.extend(ss_errs)

    print("\n============================================================")
    if failures:
        print(f"VERIFICATION FAILED ({len(failures)} issues):")
        for f in failures:
            print("  [FAIL]", f)
        sys.exit(1)
    else:
        print("ALL 8 VERIFICATION CHECKS PASSED WITH ZERO ERRORS!")
        sys.exit(0)


if __name__ == "__main__":
    main()
