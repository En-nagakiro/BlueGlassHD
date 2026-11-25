# -*- coding: utf-8 -*-
"""
Blue Glass Engine - Unified Multi-Edition BYOA (Bring Your Own Assets) Importer
===============================================================================
Imports legally owned original Tsukihime (2000) / Tsukibako / Fan-Translated
assets locally into Tsukihime_HD/game/ so the open-source repository remains
100% free of copyrighted artwork, audio, and script text.

Supported Editions & Formats:
  - Archives : arc.nsa, arc1..9.nsa (raw + LZSS), arc.sar, and loose directories
  - Scripts  : 0.txt, split 00..99.txt, encrypted nscript.dat (^ 0x84 XOR)
  - Encodings: Auto-detected UTF-8 / GB18030 (SC) / Shift-JIS CP932 (JP) / Big5 (TC)
  - Audio    : WAV / FLAC / OGG / MP3 with automatic CD-DA track02..11 offset mapping
  - Quality  : --quality fast (pure CPU, ~10s, zero GPU needed)
               --quality hd   (optional Vulkan Real-ESRGAN 4x upscale)
               --hd-pack DIR  (reuse pre-upscaled local bg/cg/tachi/word folders)
"""

import os
import re
import io
import sys
import glob
import struct
import shutil
import tempfile
import argparse
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
import numpy as np
from PIL import Image

if getattr(sys, "frozen", False):
    ROOT = os.path.dirname(os.path.abspath(sys.executable))
else:
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, os.path.join(ROOT, "scripts"))

import build_ui_theme as ui_theme
import transpile_tsukihime as transpiler

FULL_RGB_WORDS = {
    "ed_01", "ed_02", "ed_03", "ed_04", "ed_05", "ed_06", "ed_07", "ed_08",
    "ed_09", "ed_10", "ed_11", "ed_12", "ed_13", "ed_14", "ed_15", "ed_16",
    "ed_17", "end", "fin", "sinomoon", "type_moon",
}


def _decompress_lzss(data, ulen):
    """Standard NScripter LZSS decompression (comp_type == 2)."""
    ring = bytearray(256)
    rpos = 239
    out = bytearray()
    bit_idx = 0
    total_bits = len(data) * 8

    def get_bits(n):
        nonlocal bit_idx
        val = 0
        for _ in range(n):
            if bit_idx >= total_bits:
                return val
            byte = data[bit_idx >> 3]
            bit = (byte >> (7 - (bit_idx & 7))) & 1
            val = (val << 1) | bit
            bit_idx += 1
        return val

    while len(out) < ulen and bit_idx < total_bits:
        flag = get_bits(1)
        if flag:
            c = get_bits(8)
            out.append(c)
            ring[rpos] = c
            rpos = (rpos + 1) & 0xFF
        else:
            pos = get_bits(8)
            length = get_bits(4) + 2
            for k in range(length):
                if len(out) >= ulen:
                    break
                c = ring[(pos + k) & 0xFF]
                out.append(c)
                ring[rpos] = c
                rpos = (rpos + 1) & 0xFF
    return bytes(out)


class NScripterVFS:
    """Case-insensitive Virtual File System mounting arc.sar, arc*.nsa, and loose folders."""

    def __init__(self, source_dir):
        self.source_dir = os.path.abspath(source_dir)
        # norm_path -> ("disk", full_path) | ("nsa", archive_path, abs_off, clen, ulen, ctype)
        self.entries = {}
        self.mounted_sources = []
        self._mount_all()

    @staticmethod
    def _norm(p):
        return p.replace("\\", "/").lstrip("./").lower()

    def _mount_sar(self, path):
        with open(path, "rb") as f:
            cnt, data_off = struct.unpack(">HI", f.read(6))
            for _ in range(cnt):
                nb = bytearray()
                while True:
                    b = f.read(1)
                    if not b or b == b"\x00":
                        break
                    nb.extend(b)
                name = self._norm(nb.decode("cp932", errors="replace"))
                off, length = struct.unpack(">II", f.read(8))
                self.entries[name] = ("nsa", path, data_off + off, length, length, 0)
        self.mounted_sources.append(f"{os.path.basename(path)} ({cnt} files)")

    def _mount_nsa(self, path):
        with open(path, "rb") as f:
            cnt, data_off = struct.unpack(">HI", f.read(6))
            for _ in range(cnt):
                nb = bytearray()
                while True:
                    b = f.read(1)
                    if not b or b == b"\x00":
                        break
                    nb.extend(b)
                name = self._norm(nb.decode("cp932", errors="replace"))
                ctype = struct.unpack(">B", f.read(1))[0]
                off, clen, ulen = struct.unpack(">III", f.read(12))
                self.entries[name] = ("nsa", path, data_off + off, clen, ulen, ctype)
        self.mounted_sources.append(f"{os.path.basename(path)} ({cnt} files)")

    def _mount_all(self):
        # 1. SAR archive (lowest priority)
        for fn in os.listdir(self.source_dir):
            if fn.lower() == "arc.sar":
                self._mount_sar(os.path.join(self.source_dir, fn))

        # 2. arc.nsa, then arc1.nsa .. arc9.nsa (ascending override order)
        nsa_files = []
        for fn in os.listdir(self.source_dir):
            low = fn.lower()
            if low == "arc.nsa":
                nsa_files.append((0, os.path.join(self.source_dir, fn)))
            else:
                m = re.match(r"^arc(\d+)\.nsa$", low)
                if m:
                    nsa_files.append((int(m.group(1)), os.path.join(self.source_dir, fn)))
        for _, apath in sorted(nsa_files):
            self._mount_nsa(apath)

        # 3. Loose files under image/, wave/, se/, sound/ (highest priority)
        loose_cnt = 0
        for sub in ("image", "wave", "se", "sound"):
            sub_dir = None
            for d in os.listdir(self.source_dir):
                if d.lower() == sub and os.path.isdir(os.path.join(self.source_dir, d)):
                    sub_dir = os.path.join(self.source_dir, d)
                    break
            if not sub_dir:
                continue
            for root_d, _, fnames in os.walk(sub_dir):
                for fn in fnames:
                    full = os.path.join(root_d, fn)
                    rel = os.path.relpath(full, self.source_dir)
                    self.entries[self._norm(rel)] = ("disk", full)
                    loose_cnt += 1
        if loose_cnt:
            self.mounted_sources.append(f"loose directories ({loose_cnt} files)")

    def list_prefix(self, prefix):
        p = self._norm(prefix)
        return sorted(k for k in self.entries.keys() if k.startswith(p))

    def exists(self, rel_path):
        return self._norm(rel_path) in self.entries

    def read_bytes(self, rel_path):
        rec = self.entries[self._norm(rel_path)]
        if rec[0] == "disk":
            with open(rec[1], "rb") as f:
                return f.read()
        _, apath, abs_off, clen, ulen, ctype = rec
        with open(apath, "rb") as f:
            f.seek(abs_off)
            raw = f.read(clen)
        if ctype == 0:
            return raw
        if ctype == 2:
            return _decompress_lzss(raw, ulen)
        raise ValueError(f"Unsupported NSA compression type {ctype} for {rel_path}")


def discover_and_decode_script(source_dir):
    """Locate 0.txt / 00..99.txt / nscript.dat and decode automatically."""
    files = {fn.lower(): os.path.join(source_dir, fn) for fn in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, fn))}

    # 1. Plain single 0.txt or split 00.txt..99.txt
    numbered = []
    for low, full in files.items():
        if re.match(r"^\d+\.txt$", low):
            numbered.append((int(low[:-4]), low, full))
    if numbered:
        numbered.sort()
        raw_buf = bytearray()
        names = []
        for _, low, full in numbered:
            raw_buf.extend(open(full, "rb").read())
            raw_buf.extend(b"\n")
            names.append(low)
        txt, enc, lang = transpiler.decode_nscripter_bytes(bytes(raw_buf), is_encrypted=False)
        return txt, enc, lang, "+".join(names)

    # 2. Encrypted nscript.dat (^ 0x84)
    if "nscript.dat" in files:
        raw = open(files["nscript.dat"], "rb").read()
        txt, enc, lang = transpiler.decode_nscripter_bytes(raw, is_encrypted=True)
        return txt, enc, lang, "nscript.dat (^0x84)"

    raise FileNotFoundError(
        f"No NScripter script (0.txt / 00.txt / nscript.dat) found in: {source_dir}"
    )


def split_nscripter_alpha_image(im_rgb):
    """
    Split an NScripter ':a;' double-width side-by-side image (left=RGB, right=inverted alpha mask)
    into a clean RGBA PIL Image with JPEG edge cleanup.
    """
    arr = np.array(im_rgb.convert("RGB"), dtype=np.uint8)
    h, w, _ = arr.shape
    half = w // 2
    rgb = arr[:, :half, :]
    mask_rgb = arr[:, half : half * 2, :]
    # Inverted grayscale alpha: white (255) = transparent, black (0) = opaque
    gray = (0.299 * mask_rgb[:, :, 0] + 0.587 * mask_rgb[:, :, 1] + 0.114 * mask_rgb[:, :, 2])
    alpha = np.clip(255.0 - gray, 0.0, 255.0)
    # Snap JPEG mosquito noise near pure 0 / pure 255
    alpha = np.where(alpha < 12.0, 0.0, np.where(alpha > 243.0, 255.0, alpha)).astype(np.uint8)
    rgba = np.dstack([rgb, alpha])
    return Image.fromarray(rgba, mode="RGBA")


def import_audio(vfs, source_dir, target_game):
    """
    Import original SE (from VFS wave/se_*) and multi-format BGM (WAV/FLAC/OGG/MP3)
    with automatic CD-DA track02..11 offset detection.
    Returns audio_ext_map: {"01": "01.wav", "se_01": "se_01.wav", ...}
    """
    audio_dst = os.path.join(target_game, "audio")
    os.makedirs(audio_dst, exist_ok=True)
    ext_map = {}

    # 1. Extract SE from VFS (wave/se_*, se/*)
    se_cnt = 0
    for key in vfs.list_prefix("wave/") + vfs.list_prefix("se/"):
        ext = os.path.splitext(key)[1].lower()
        if ext not in (".wav", ".ogg", ".mp3"):
            continue
        bname = os.path.basename(key).lower()
        stem = os.path.splitext(bname)[0]
        dst = os.path.join(audio_dst, bname)
        with open(dst, "wb") as f:
            f.write(vfs.read_bytes(key))
        ext_map[stem] = bname
        se_cnt += 1

    # 2. Discover BGM tracks across bgm/, cd/, music/, audio/, and root
    bgm_candidates = {}  # track_int -> (priority, src_path, ext)
    search_dirs = [source_dir]
    for sub in os.listdir(source_dir):
        if sub.lower() in ("bgm", "cd", "music", "audio") and os.path.isdir(os.path.join(source_dir, sub)):
            search_dirs.append(os.path.join(source_dir, sub))

    ext_prio = {".wav": 4, ".flac": 3, ".ogg": 2, ".mp3": 1}
    for sd in search_dirs:
        for fn in os.listdir(sd):
            full = os.path.join(sd, fn)
            if not os.path.isfile(full):
                continue
            ext = os.path.splitext(fn)[1].lower()
            if ext not in ext_prio:
                continue
            stem = os.path.splitext(fn)[0].lower()
            m = re.match(r"^(?:track|bgm|cd|m)?[_-]?0*(\d{1,2})$", stem)
            if not m:
                continue
            num = int(m.group(1))
            if 1 <= num <= 12:
                prio = ext_prio[ext]
                if num not in bgm_candidates or prio > bgm_candidates[num][0]:
                    bgm_candidates[num] = (prio, full, ext)

    # Detect CD-DA Track 1 data-track offset (track02..11 without track01!)
    cd_offset = 0
    if 1 not in bgm_candidates and 2 in bgm_candidates and 11 in bgm_candidates:
        cd_offset = -1
        print("      [INFO] Detected CD-DA track02..11 offset; remapping to 01..10.")

    bgm_cnt = 0
    for raw_num, (_, src_p, ext) in sorted(bgm_candidates.items()):
        mapped = raw_num + cd_offset
        if 1 <= mapped <= 10:
            dst_name = f"{mapped:02d}{ext}"
            shutil.copy2(src_p, os.path.join(audio_dst, dst_name))
            ext_map[f"{mapped:02d}"] = dst_name
            bgm_cnt += 1

    print(f"[2/6] Audio imported: {se_cnt} SE tracks, {bgm_cnt}/10 BGM tracks.")
    if bgm_cnt < 10:
        print("      [NOTE] Some BGM tracks were not found; game will still run cleanly with available tracks.")
    return ext_map


def _find_realesrgan():
    local = os.path.join(ROOT, "tools", "realesrgan", "realesrgan-ncnn-vulkan.exe")
    if os.path.exists(local):
        return local, os.path.join(ROOT, "tools", "realesrgan", "models")
    in_path = shutil.which("realesrgan-ncnn-vulkan")
    if in_path:
        return in_path, None
    return None, None


def import_images(vfs, target_game, quality="fast", hd_pack=None):
    """Extract and convert all BG / CG / Tachi / Word assets into lowercase WebP."""
    img_root = os.path.join(target_game, "images")
    sub_dirs = {k: os.path.join(img_root, k) for k in ("bg", "cg", "tachi", "word")}
    for d in sub_dirs.values():
        os.makedirs(d, exist_ok=True)

    # Optional pre-upscaled local HD pack fast-copy
    if hd_pack and os.path.isdir(hd_pack):
        copied = 0
        for cat in ("bg", "cg", "tachi", "word"):
            src_c = os.path.join(hd_pack, cat)
            if not os.path.isdir(src_c):
                continue
            for fn in os.listdir(src_c):
                if fn.lower().endswith(".webp"):
                    shutil.copy2(os.path.join(src_c, fn), os.path.join(sub_dirs[cat], fn.lower()))
                    copied += 1
        if copied >= 600:
            print(f"[3/6] Imported {copied} pre-upscaled WebP images from --hd-pack.")
            return copied

    # Collect VFS image jobs: (vfs_key, category, stem, is_alpha_split)
    jobs = []
    cat_map = [
        ("image/bg/",    "bg",    False),
        ("image/event/", "cg",    False),
        ("image/tachi/", "tachi", True),
        ("image/word/",  "word",  None),  # Determined per-file via FULL_RGB_WORDS
    ]
    for prefix, cat, alpha_mode in cat_map:
        for key in vfs.list_prefix(prefix):
            ext = os.path.splitext(key)[1].lower()
            if ext not in (".jpg", ".jpeg", ".png", ".bmp"):
                continue
            stem = os.path.splitext(os.path.basename(key))[0].lower()
            if cat == "word":
                is_alpha = stem not in FULL_RGB_WORDS
            else:
                is_alpha = bool(alpha_mode)
            jobs.append((key, cat, stem, is_alpha))

    use_hd = False
    esrgan_exe, esrgan_models = None, None
    if quality == "hd":
        esrgan_exe, esrgan_models = _find_realesrgan()
        if esrgan_exe:
            use_hd = True
        else:
            print("      [WARN] realesrgan-ncnn-vulkan not found; falling back cleanly to --quality fast (CPU).")

    if not use_hd:
        print(f"[3/6] Extracting & converting {len(jobs)} images (CPU Fast Mode -> WebP)...")

        def worker(job):
            key, cat, stem, is_alpha = job
            raw = vfs.read_bytes(key)
            im = Image.open(io.BytesIO(raw))
            out_path = os.path.join(sub_dirs[cat], f"{stem}.webp")
            if is_alpha:
                rgba = split_nscripter_alpha_image(im)
                rgba.save(out_path, "WEBP", lossless=True, method=4)
            else:
                im.convert("RGB").save(out_path, "WEBP", quality=92, method=4)
            return out_path

        done = 0
        total_jobs = len(jobs)
        step_mark = max(1, total_jobs // 10)
        with ThreadPoolExecutor(max_workers=max(4, os.cpu_count() or 4)) as ex:
            futs = [ex.submit(worker, j) for j in jobs]
            for f in as_completed(futs):
                f.result()
                done += 1
                if done == total_jobs or (done % step_mark == 0):
                    pct = int(round(done * 100.0 / max(1, total_jobs)))
                    print(f"      [3/6] Progress: {done}/{total_jobs} ({pct}%)")
        print(f"      [OK] Converted {done} images cleanly into {img_root}.")
        return done

    # Optional Vulkan Real-ESRGAN 4x HD Pipeline (RGB + Alpha cleanly separated!)
    print(f"[3/6] Running Vulkan Real-ESRGAN 4x HD Upscale on {len(jobs)} images...")
    tmp_dir = tempfile.mkdtemp(prefix="byoa_esrgan_")
    try:
        in_rgb = os.path.join(tmp_dir, "in_rgb")
        out_rgb = os.path.join(tmp_dir, "out_rgb")
        in_mask = os.path.join(tmp_dir, "in_mask")
        out_mask = os.path.join(tmp_dir, "out_mask")
        for d in (in_rgb, out_rgb, in_mask, out_mask):
            os.makedirs(d, exist_ok=True)

        meta = []
        for idx, (key, cat, stem, is_alpha) in enumerate(jobs):
            raw = vfs.read_bytes(key)
            im = Image.open(io.BytesIO(raw)).convert("RGB")
            tag = f"{idx:04d}_{cat}_{stem}"
            if is_alpha:
                w, h = im.size
                im.crop((0, 0, w // 2, h)).save(os.path.join(in_rgb, f"{tag}.png"))
                im.crop((w // 2, 0, (w // 2) * 2, h)).save(os.path.join(in_mask, f"{tag}.png"))
            else:
                im.save(os.path.join(in_rgb, f"{tag}.png"))
            meta.append((tag, cat, stem, is_alpha))

        def run_esrgan(src_d, dst_d):
            cmd = [esrgan_exe, "-i", src_d, "-o", dst_d, "-n", "realesrgan-x4plus-anime", "-f", "png"]
            if esrgan_models and os.path.isdir(esrgan_models):
                cmd.extend(["-m", esrgan_models])
            res = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace")
            if res.returncode != 0:
                raise RuntimeError(f"Real-ESRGAN failed: {res.stderr[:300]}")

        run_esrgan(in_rgb, out_rgb)
        if os.listdir(in_mask):
            run_esrgan(in_mask, out_mask)

        def pack_hd(rec):
            tag, cat, stem, is_alpha = rec
            rgb_im = Image.open(os.path.join(out_rgb, f"{tag}.png")).convert("RGB")
            out_path = os.path.join(sub_dirs[cat], f"{stem}.webp")
            if is_alpha:
                m_im = Image.open(os.path.join(out_mask, f"{tag}.png")).convert("L")
                if m_im.size != rgb_im.size:
                    m_im = m_im.resize(rgb_im.size, Image.Resampling.LANCZOS)
                a = np.clip(255.0 - np.array(m_im, dtype=np.float32), 0.0, 255.0)
                a = np.where(a < 14.0, 0.0, np.where(a > 242.0, 255.0, a)).astype(np.uint8)
                rgba = Image.fromarray(np.dstack([np.array(rgb_im), a]), mode="RGBA")
                rgba.save(out_path, "WEBP", lossless=True, method=4)
            else:
                rgb_im.save(out_path, "WEBP", quality=92, method=4)

        with ThreadPoolExecutor(max_workers=max(4, os.cpu_count() or 4)) as ex:
            list(ex.map(pack_hd, meta))
        print(f"      [OK] 4x AI-upscaled {len(meta)} images into {img_root}.")
        return len(meta)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def generate_image_definitions(target_game):
    """Write core/image_definitions.rpy dynamically matching extracted WebP inventory."""
    core_dir = os.path.join(target_game, "core")
    os.makedirs(core_dir, exist_ok=True)
    out_path = os.path.join(core_dir, "image_definitions.rpy")

    def list_stems(sub):
        d = os.path.join(target_game, "images", sub)
        if not os.path.isdir(d):
            return []
        return sorted(os.path.splitext(f)[0] for f in os.listdir(d) if f.endswith(".webp"))

    bgs = list_stems("bg")
    cgs = list_stems("cg")
    words = list_stems("word")
    tachis = list_stems("tachi")

    lines = [
        "## ==============================================================================",
        "## Auto-generated BYOA Image Registry (core/image_definitions.rpy)",
        "## ==============================================================================",
        "",
        'image black = Solid("#000000")',
        'image white = Solid("#ffffff")',
        'image red = Solid("#880000")',
        'image blue_flash = Solid("#0000ff")',
        "",
        "## Backgrounds",
    ]
    lines.extend(f'image bg {b} = "images/bg/{b}.webp"' for b in bgs)
    lines.append("\n## Event CGs")
    lines.extend(f'image cg {c} = "images/cg/{c}.webp"' for c in cgs)
    lines.append("\n## Word Cards & Ending Credits")
    lines.extend(f'image word {w} = "images/word/{w}.webp"' for w in words)

    lines.append("\ninit -5 python:")
    lines.append("    TACHI_FILES = {")
    lines.extend(f'        "{t}": "images/tachi/{t}.webp",' for t in tachis)
    lines.append("    }")
    lines.append("    BG_FILES = {")
    lines.extend(f'        "{b}": "images/bg/{b}.webp",' for b in bgs)
    lines.append("    }")
    lines.append("    CG_FILES = {")
    lines.extend(f'        "{c}": "images/cg/{c}.webp",' for c in cgs)
    lines.append("    }")
    lines.append("    WORD_FILES = {")
    lines.extend(f'        "{w}": "images/word/{w}.webp",' for w in words)
    lines.append("    }")
    lines.append("    FULL_RGB_WORDS = " + repr(sorted(FULL_RGB_WORDS)))

    with open(out_path, "w", encoding="utf-8", newline="\n") as fp:
        fp.write("\n".join(lines) + "\n")
    print(f"[4/6] Generated image registry: bg={len(bgs)}, cg={len(cgs)}, tachi={len(tachis)}, word={len(words)}.")


def synthesize_user_derived_gui(vfs, target_game):
    """Build user-derived title moon/kanji & 10 heroine portraits locally from imported assets."""
    gui_dir = os.path.join(target_game, "gui")
    os.makedirs(gui_dir, exist_ok=True)

    # 1. Extract original title1.jpg from VFS and synthesize both Default & Eclipse moon/kanji
    title_key = None
    for cand in ("image/title/title1.jpg", "image/title/title1.png", "image/title/title1.bmp"):
        if vfs.exists(cand):
            title_key = cand
            break
    if title_key:
        title1_pil = Image.open(io.BytesIO(vfs.read_bytes(title_key)))
        ui_theme.build_user_derived_title_art(title1_pil, out_gui_dir=gui_dir)
    else:
        print("      [WARN] image/title/title1.jpg not found in archive; keeping fallback title art if present.")

    # 2. Synthesize 10 feathered heroine portraits from extracted tachi sprites
    ui_theme.build_heroine_portrait_assets(game_dir=target_game)

    # 3. Ensure pure-Python synthesized open-source UI chimes exist
    ui_theme.build_original_ui_audio(audio_dir=os.path.join(target_game, "audio"))

    # 4. Write gitignored local BYOA splash epigraph (keeps open-source Git repo quote-free)
    meta_path = os.path.join(target_game, "core", "byoa_meta.rpy")
    os.makedirs(os.path.dirname(meta_path), exist_ok=True)
    with open(meta_path, "w", encoding="utf-8", newline="\n") as mf:
        mf.write(
            '## Locally generated BYOA splash metadata (excluded from Git via .gitignore)\n'
            'init 1 python:\n'
            '    BYOA_SPLASH_QUOTE = "——ああ、今夜は、こんなにも月が綺麗だ。"\n'
            '    BYOA_SPLASH_SUB = "Blue Blue Glass Moon, Under The Crimson Air."\n'
        )
    print("[5/6] Built locally derived title art, heroine portraits & splash metadata.")


def main():
    ap = argparse.ArgumentParser(
        description="Blue Glass Engine - Local BYOA Importer for legally owned Tsukihime (2000) copies."
    )
    ap.add_argument("--source", required=True, help="Path to user's original Tsukihime (2000) directory")
    ap.add_argument("--target", default=os.path.join(ROOT, "Tsukihime_HD"), help="Target Ren'Py project directory")
    ap.add_argument("--quality", choices=("fast", "hd"), default="fast", help="fast = CPU WebP (~10s), hd = Vulkan Real-ESRGAN 4x")
    ap.add_argument("--hd-pack", default="", help="Optional path to an existing local upscaled images/ folder")
    args = ap.parse_args()

    src_dir = os.path.abspath(args.source)
    target_proj = os.path.abspath(args.target)
    target_game = os.path.join(target_proj, "game")

    if not os.path.isdir(src_dir):
        print(f"[ERROR] Source directory does not exist: {src_dir}")
        sys.exit(1)

    if not (
        os.path.isdir(os.path.join(target_game, "ui"))
        and os.path.isdir(os.path.join(target_game, "core"))
    ):
        print(
            f"[ERROR] Target directory does not contain the open-source engine core "
            f"(expected game/ui and game/core under: {target_proj})"
        )
        sys.exit(2)

    print("============================================================")
    print("Blue Glass Engine - BYOA Local Asset Importer")
    print(f"  Source : {src_dir}")
    print(f"  Target : {target_proj}")
    print(f"  Quality: {args.quality}")
    print("============================================================")

    # 1. Mount NScripter VFS & decode multi-edition script
    vfs = NScripterVFS(src_dir)
    if not vfs.entries:
        print(f"[ERROR] No NScripter archives (arc.nsa/arc.sar) or image/ directories found in {src_dir}")
        sys.exit(1)
    print(f"[1/6] Mounted VFS ({len(vfs.entries)} files): {', '.join(vfs.mounted_sources)}")

    script_text, enc, lang, script_src = discover_and_decode_script(src_dir)
    print(f"      Script detected: {script_src} | encoding={enc} | language={lang}")

    # 2. Import Audio (SE + multi-format BGM)
    audio_ext_map = import_audio(vfs, src_dir, target_game)

    # 3. Extract & convert images (Fast CPU or HD Vulkan)
    import_images(vfs, target_game, quality=args.quality, hd_pack=args.hd_pack or None)

    # 4. Generate dynamic image registry
    generate_image_definitions(target_game)

    # 5. Synthesize user-derived title moon/kanji & heroine portraits
    synthesize_user_derived_gui(vfs, target_game)

    # 6. Transpile NScripter script -> Ren'Py NVL story modules
    print("[6/6] Transpiling script to Ren'Py 8 NVL modules...")
    t = transpiler.TsukihimeASTTranspiler(
        out_game_dir=target_game,
        script_text=script_text,
        edition_lang=lang,
        audio_ext_map=audio_ext_map,
    )
    t.transpile_all()

    print("\n============================================================")
    print("BYOA IMPORT COMPLETE! Launch the game to start playing.")
    print("============================================================")


if __name__ == "__main__":
    main()
