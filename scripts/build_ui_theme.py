# -*- coding: utf-8 -*-
"""
Tsukihime Classic HD - Plan A "Frosted Mist" (薄雾琉璃) UI Asset Builder
=========================================================================
Generates:
  1. Verifies 100% open-source (SIL OFL 1.1 / IPA v1.0) fonts in game/fonts/
  2. Option B Asymmetric Title Backdrop (gui/main_menu.webp)
  3. Silky 16-bit dithered Frosted Mist inner backdrop (gui/game_menu.webp) - ZERO ghost blobs!
  4. Soft slate-mist Tsukihime-R Flowchart backdrop & soft glow dividers
  5. Full 2x-supersampled 9-slice rounded frosted-glass cards, capsule pills,
     iOS/macOS pill toggle switches, circular-thumb sliders, soft dots & aspect schematics
"""

import os
import io
import struct
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAME = os.path.join(ROOT, "Tsukihime_HD", "game")
GUI_DIR = os.path.join(GAME, "gui")
MIST_DIR = os.path.join(GUI_DIR, "mist")
FONTS_DIR = os.path.join(GAME, "fonts")
NSA_PATH = os.environ.get("TSUKIHIME_NSA", "")


def bundle_fonts():
    """Verify the 100% open-source (SIL OFL 1.1 / IPA v1.0) bundled font suite in game/fonts/."""
    os.makedirs(FONTS_DIR, exist_ok=True)
    required = [
        "lxgw_xihei.ttf",
        "lxgw_xihei_screen.ttf",
        "notoserif_sc.otf",
        "lxgw_wenkai.ttf",
        "notosans_med.otf",
        "lora_reg.ttf",
        "lora_italic.ttf",
        "LICENSES.txt",
    ]
    for fn in required:
        p = os.path.join(FONTS_DIR, fn)
        if os.path.exists(p):
            print(f"[OK] Open-source font asset present: fonts/{fn}")
        else:
            print(f"[WARN] Missing open-source font asset: fonts/{fn}")


def draw_rr_sprite(w, h, radius, fill, outline=None, outline_w=1, top_highlight=None, pad=0, shadow=None):
    """Render a 2x supersampled crisp anti-aliased rounded-rectangle RGBA sprite."""
    S = 2
    tw, th = (w + pad * 2) * S, (h + pad * 2) * S
    im = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    if shadow:
        scol, sblur, soffy = shadow
        sl = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
        sd = ImageDraw.Draw(sl)
        sd.rounded_rectangle(
            [pad * S, (pad + soffy) * S, (pad + w) * S - 1, (pad + h + soffy) * S - 1],
            radius=radius * S, fill=scol
        )
        sl = sl.filter(ImageFilter.GaussianBlur(radius=sblur * S))
        im.alpha_composite(sl)

    d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = pad * S, pad * S, (pad + w) * S - 1, (pad + h) * S - 1
    d.rounded_rectangle([x0, y0, x1, y1], radius=radius * S, fill=fill)

    if top_highlight:
        # Subtle inner specular top highlight sheen for frosted glass realism
        hl = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
        hd = ImageDraw.Draw(hl)
        hd.rounded_rectangle([x0 + S, y0 + S, x1 - S, y0 + S * 3], radius=max(1, (radius - 1) * S), fill=top_highlight)
        im.alpha_composite(hl)

    if outline:
        d = ImageDraw.Draw(im)
        d.rounded_rectangle(
            [x0, y0, x1, y1], radius=radius * S, fill=None,
            outline=outline, width=max(1, int(round(outline_w * S)))
        )

    return im.resize((w + pad * 2, h + pad * 2), Image.Resampling.LANCZOS)


def make_silky_mesh(w, h, c_tl, c_br, glow_pos, glow_col, glow_rad, seed=11, grain=0.9):
    """Ultra-smooth 16-bit dithered ambient mesh gradient with zero banding and zero ghost blobs."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    nx = xx / float(w)
    ny = yy / float(h)
    t = np.clip(0.55 * nx + 0.45 * ny, 0.0, 1.0)
    t = t * t * (3.0 - 2.0 * t)

    arr = np.zeros((h, w, 3), dtype=np.float32)
    for ch in range(3):
        arr[:, :, ch] = c_tl[ch] * (1.0 - t) + c_br[ch] * t

    gx, gy = glow_pos[0] * w, glow_pos[1] * h
    dist = np.sqrt(((xx - gx) / (w * glow_rad)) ** 2 + ((yy - gy) / (h * glow_rad * 1.3)) ** 2)
    g_w = np.exp(-(dist ** 2))
    for ch in range(3):
        arr[:, :, ch] += glow_col[ch] * g_w

    # Second subtle bottom-left mist lift for natural balance
    gx2, gy2 = 0.16 * w, 0.85 * h
    dist2 = np.sqrt(((xx - gx2) / (w * 0.48)) ** 2 + ((yy - gy2) / (h * 0.55)) ** 2)
    g_w2 = np.exp(-(dist2 ** 2))
    arr[:, :, 0] += 6.0 * g_w2
    arr[:, :, 1] += 9.0 * g_w2
    arr[:, :, 2] += 14.0 * g_w2

    rng = np.random.default_rng(seed)
    arr += rng.normal(0.0, grain, size=(h, w, 3)).astype(np.float32)
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), mode="RGB")


def build_frosted_mist_sprites():
    os.makedirs(MIST_DIR, exist_ok=True)
    slider_dir = os.path.join(GUI_DIR, "slider")
    os.makedirs(slider_dir, exist_ok=True)

    # 1. Floating Left Rail & Frosted Glass Cards (9-slice ready: 96x96 with 24px borders)
    draw_rr_sprite(96, 96, 20, fill=(255, 255, 255, 13), outline=(220, 234, 250, 26), outline_w=1).save(os.path.join(MIST_DIR, "rail.png"))
    draw_rr_sprite(96, 96, 18, fill=(255, 255, 255, 14), outline=(220, 234, 250, 26), outline_w=1).save(os.path.join(MIST_DIR, "card.png"))
    draw_rr_sprite(96, 96, 18, fill=(255, 255, 255, 24), outline=(218, 234, 250, 56), outline_w=1).save(os.path.join(MIST_DIR, "card_hover.png"))
    draw_rr_sprite(96, 96, 18, fill=(158, 194, 228, 36), outline=(174, 208, 238, 145), outline_w=1.5).save(os.path.join(MIST_DIR, "card_sel.png"))
    draw_rr_sprite(96, 96, 18, fill=(224, 200, 144, 30), outline=(228, 206, 152, 130), outline_w=1.5).save(os.path.join(MIST_DIR, "card_gold.png"))
    draw_rr_sprite(96, 96, 22, fill=(20, 26, 38, 244), outline=(216, 232, 248, 52), outline_w=1).save(os.path.join(MIST_DIR, "modal.png"))

    # 2. Segmented Capsule Track & Smooth Active/Hover/Danger/Gold Pills (80x48 & 80x40)
    draw_rr_sprite(80, 48, 24, fill=(8, 11, 18, 128), outline=(220, 234, 250, 24), outline_w=1).save(os.path.join(MIST_DIR, "seg_track.png"))
    draw_rr_sprite(80, 40, 20, fill=(168, 200, 232, 50), outline=(194, 220, 246, 108), outline_w=1).save(os.path.join(MIST_DIR, "pill_active.png"))
    draw_rr_sprite(80, 40, 20, fill=(255, 255, 255, 16), outline=(220, 234, 250, 34), outline_w=1).save(os.path.join(MIST_DIR, "pill_idle.png"))
    draw_rr_sprite(80, 40, 20, fill=(255, 255, 255, 28), outline=(220, 234, 250, 62), outline_w=1).save(os.path.join(MIST_DIR, "pill_hover.png"))
    draw_rr_sprite(80, 40, 20, fill=(212, 132, 146, 48), outline=(226, 156, 168, 118), outline_w=1).save(os.path.join(MIST_DIR, "pill_rose.png"))
    draw_rr_sprite(80, 40, 20, fill=(220, 196, 138, 44), outline=(234, 212, 158, 120), outline_w=1).save(os.path.join(MIST_DIR, "pill_gold.png"))

    # 3. Navigation & Tracklist Soft Rounded Capsules (80x46)
    draw_rr_sprite(80, 46, 14, fill=(168, 200, 232, 38), outline=(186, 216, 244, 82), outline_w=1).save(os.path.join(MIST_DIR, "nav_sel.png"))
    draw_rr_sprite(80, 46, 14, fill=(255, 255, 255, 15), outline=None).save(os.path.join(MIST_DIR, "nav_hover.png"))
    draw_rr_sprite(80, 46, 14, fill=(214, 134, 148, 28), outline=(226, 154, 168, 56), outline_w=1).save(os.path.join(MIST_DIR, "nav_rose_hover.png"))
    draw_rr_sprite(80, 46, 14, fill=(224, 200, 144, 30), outline=(234, 212, 158, 72), outline_w=1).save(os.path.join(MIST_DIR, "nav_gold_hover.png"))

    # 4. In-Game Choice Frosted Rounded Bars (96x66)
    draw_rr_sprite(96, 66, 16, fill=(14, 20, 30, 214), outline=(214, 228, 246, 52), outline_w=1).save(os.path.join(MIST_DIR, "choice_idle.png"))
    draw_rr_sprite(96, 66, 16, fill=(32, 46, 68, 234), outline=(174, 208, 238, 138), outline_w=1.5).save(os.path.join(MIST_DIR, "choice_hover.png"))

    # 5. Quick Menu Soft Floating Capsule
    draw_rr_sprite(80, 36, 18, fill=(12, 16, 24, 184), outline=(218, 232, 248, 30), outline_w=1).save(os.path.join(MIST_DIR, "quick_pill.png"))

    # 6. Modern Rounded Capsule Toggle Switches (60x32, 2x supersampled!)
    def make_toggle(on, track_col, fname):
        S = 2
        w, h = 60, 32
        im = Image.new("RGBA", (w * S, h * S), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([1, 1, w * S - 2, h * S - 2], radius=16 * S, fill=track_col, outline=(220, 234, 250, 44), width=2)
        # Soft drop shadow + pure white circular knob
        kx = (w - 27) * S if on else 5 * S
        ky = 5 * S
        kd = 22 * S
        sh = Image.new("RGBA", (w * S, h * S), (0, 0, 0, 0))
        sd = ImageDraw.Draw(sh)
        sd.ellipse([kx, ky + 3, kx + kd, ky + kd + 3], fill=(0, 0, 0, 65))
        sh = sh.filter(ImageFilter.GaussianBlur(radius=4))
        im.alpha_composite(sh)
        d = ImageDraw.Draw(im)
        d.ellipse([kx, ky, kx + kd, ky + kd], fill=(246, 250, 255, 255))
        im.resize((w, h), Image.Resampling.LANCZOS).save(os.path.join(MIST_DIR, fname))

    make_toggle(True,  (146, 184, 218, 235), "toggle_on.png")
    make_toggle(False, (255, 255, 255, 30),  "toggle_off.png")
    make_toggle(True,  (212, 188, 134, 230), "toggle_gold_on.png")
    make_toggle(True,  (208, 134, 146, 230), "toggle_rose_on.png")

    # 7. Smooth Rounded-Cap Sliders & Circular Soft-Shadow Knob (slider/hairline_*.png)
    S = 2
    # Filled track (32x22 -> rounded 6px bar centered vertically y=8..13)
    im = Image.new("RGBA", (32 * S, 22 * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 8 * S, 32 * S - 1, 14 * S - 1], radius=3 * S, fill=(162, 198, 230, 240))
    im.resize((32, 22), Image.Resampling.LANCZOS).save(os.path.join(slider_dir, "hairline_fill.png"))

    # Unfilled track
    im = Image.new("RGBA", (32 * S, 22 * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 8 * S, 32 * S - 1, 14 * S - 1], radius=3 * S, fill=(220, 232, 248, 38))
    im.resize((32, 22), Image.Resampling.LANCZOS).save(os.path.join(slider_dir, "hairline_track.png"))

    # Circular soft-shadow white thumb (22x22)
    def make_thumb(ring_col, radius_px, fname):
        tw = 22
        im = Image.new("RGBA", (tw * S, tw * S), (0, 0, 0, 0))
        sh = Image.new("RGBA", (tw * S, tw * S), (0, 0, 0, 0))
        cx = (tw * S) // 2
        r = radius_px * S
        ImageDraw.Draw(sh).ellipse([cx - r, cx - r + 3, cx + r, cx + r + 3], fill=(0, 0, 0, 75))
        im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(radius=4)))
        ImageDraw.Draw(im).ellipse([cx - r, cx - r, cx + r, cx + r], fill=(246, 250, 255, 255), outline=ring_col, width=4)
        im.resize((tw, tw), Image.Resampling.LANCZOS).save(os.path.join(slider_dir, fname))

    make_thumb((162, 198, 230, 255), 8, "hairline_thumb.png")
    make_thumb((212, 232, 250, 255), 9, "hairline_thumb_hover.png")

    # 8. Soft Anti-Aliased Indicator Dots (12x12)
    for col, fname in [
        ((162, 198, 230, 255), "dot_accent.png"),
        ((224, 200, 144, 255), "dot_gold.png"),
        ((214, 144, 156, 255), "dot_rose.png"),
        ((134, 218, 190, 255), "dot_mint.png"),
        ((108, 124, 144, 180), "dot_dim.png"),
    ]:
        im = Image.new("RGBA", (24, 24), (0, 0, 0, 0))
        ImageDraw.Draw(im).ellipse([4, 4, 20, 20], fill=col)
        im.resize((12, 12), Image.Resampling.LANCZOS).save(os.path.join(MIST_DIR, fname))

    # 8b. High-Contrast Soft Mint Pill & Luminous Outer Glow Halos for Flowchart
    draw_rr_sprite(80, 40, 20, fill=(14, 42, 36, 232), outline=(146, 236, 206, 220), outline_w=1.5).save(os.path.join(MIST_DIR, "pill_mint.png"))

    def make_glow_halo(ring_col, glow_col, fname):
        """Render a rich luminous outer-bloom halo frame (pad=14px) that stays unmistakably visible around thumbnails."""
        S = 2
        w, h, pad, rad = 96, 72, 14, 10
        tw, th = (w + pad * 2) * S, (h + pad * 2) * S
        im = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
        x0, y0, x1, y1 = pad * S, pad * S, (pad + w) * S - 1, (pad + h) * S - 1
        # Wide soft bloom layer 1
        g1 = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
        ImageDraw.Draw(g1).rounded_rectangle([x0 - 3 * S, y0 - 3 * S, x1 + 3 * S, y1 + 3 * S], radius=(rad + 3) * S, fill=glow_col)
        im.alpha_composite(g1.filter(ImageFilter.GaussianBlur(radius=9 * S)))
        # Tight bright inner bloom layer 2
        g2 = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
        ImageDraw.Draw(g2).rounded_rectangle([x0 - S, y0 - S, x1 + S, y1 + S], radius=(rad + 1) * S, outline=ring_col, width=5 * S)
        im.alpha_composite(g2.filter(ImageFilter.GaussianBlur(radius=3 * S)))
        # Crisp bright edge outline
        ImageDraw.Draw(im).rounded_rectangle([x0 - S, y0 - S, x1 + S, y1 + S], radius=(rad + 1) * S, outline=ring_col, width=3 * S)
        im.resize((w + pad * 2, h + pad * 2), Image.Resampling.LANCZOS).save(os.path.join(MIST_DIR, fname))

    make_glow_halo((146, 242, 210, 255), (108, 228, 190, 145), "fc_here_halo.png")
    make_glow_halo((166, 216, 255, 255), (124, 188, 244, 130), "fc_sel_halo.png")

    # 9. Rounded Miniature 16:9 Aspect Ratio Schematic Illustrations (160x90)
    def make_schematic(kind, selected, fname):
        S = 2
        w, h = 160, 90
        im = Image.new("RGBA", (w * S, h * S), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        inner_col = (154, 192, 226, 240) if selected else (106, 134, 166, 200)
        border_col = (210, 226, 244, 135) if selected else (200, 218, 238, 75)
        if kind == "ambient":
            d.rounded_rectangle([2, 2, w * S - 3, h * S - 3], radius=10 * S, fill=(68, 86, 110, 175), outline=border_col, width=2)
            d.rounded_rectangle([20 * S, 4 * S, (w - 20) * S, (h - 4) * S], radius=5 * S, fill=inner_col)
        elif kind == "black":
            d.rounded_rectangle([2, 2, w * S - 3, h * S - 3], radius=10 * S, fill=(14, 17, 24, 225), outline=border_col, width=2)
            d.rounded_rectangle([20 * S, 4 * S, (w - 20) * S, (h - 4) * S], radius=5 * S, fill=inner_col)
        else:
            d.rounded_rectangle([2, 2, w * S - 3, h * S - 3], radius=10 * S, fill=inner_col, outline=border_col, width=2)
        im.resize((w, h), Image.Resampling.LANCZOS).save(os.path.join(MIST_DIR, fname))

    for k in ("ambient", "black", "full"):
        make_schematic(k, False, f"sch_{k}.png")
        make_schematic(k, True,  f"sch_{k}_sel.png")

    # 10. Softened Flowchart Glow Divider & Ribbon (halos built in 8b above!)
    draw_rr_sprite(96, 72, 10, fill=(0, 0, 0, 0), outline=(218, 198, 146, 165), outline_w=1, pad=2).save(os.path.join(MIST_DIR, "fc_gold_frame.png"))

    dw, dh = 1340, 7
    dl = np.zeros((dh, dw, 4), dtype=np.float32)
    dx = np.linspace(0.0, 1.0, dw, dtype=np.float32)
    horiz = np.clip(dx / 0.04, 0.0, 1.0) * (1.0 - np.clip((dx - 0.55) / 0.45, 0.0, 1.0) ** 1.3)
    vert_glow = np.array([0.10, 0.26, 0.52, 0.92, 0.52, 0.26, 0.10], dtype=np.float32)[:, None]
    dl[:, :, 0] = 148.0
    dl[:, :, 1] = 186.0
    dl[:, :, 2] = 222.0
    dl[:, :, 3] = np.clip(vert_glow * horiz[None, :] * 135.0, 0, 255)
    dl[3, :, 0] = 178.0
    dl[3, :, 1] = 210.0
    dl[3, :, 2] = 238.0
    dl[3, :, 3] = np.clip(horiz * 170.0, 0, 255)
    Image.fromarray(dl.astype(np.uint8), mode="RGBA").save(os.path.join(GUI_DIR, "fc_day_line.png"))

    rw, rh = 128, 30
    rb = Image.new("RGBA", (rw, rh), (0, 0, 0, 0))
    rd = ImageDraw.Draw(rb)
    rd.polygon([(0, 0), (rw, 0), (rw, rh), (22, rh)], fill=(58, 84, 118, 232))
    rd.line([(0, 0), (22, rh - 1)], fill=(176, 206, 236, 150), width=1)
    rd.line([(22, rh - 1), (rw, rh - 1)], fill=(176, 206, 236, 130), width=1)
    rb.save(os.path.join(GUI_DIR, "fc_ribbon.png"))

    print("[OK] Built all 2x-supersampled Plan A Frosted Mist glass sprites, toggles & sliders")


def build_silky_inner_backdrops():
    W, H = 1920, 1080
    # 1. Pure Frosted Mist Inner Backdrop (gui/game_menu.webp) - ZERO muddy moon/kanji ghost blob!
    gm = make_silky_mesh(W, H, (16, 20, 28), (27, 34, 46), (0.78, 0.24), (22, 34, 52), 0.56, seed=11, grain=0.85)
    gm_out = os.path.join(GUI_DIR, "game_menu.webp")
    gm.save(gm_out, "WEBP", quality=94, method=4)
    print(f"[OK] Built pure silky Frosted Mist Backdrop: {gm_out} ({os.path.getsize(gm_out)//1024} KB)")

    # 2. Softened Dark Slate-Mist Flowchart Backdrop (gui/flowchart_bg.webp)
    fc = make_silky_mesh(W, H, (10, 13, 20), (20, 26, 38), (0.82, 0.30), (16, 26, 40), 0.58, seed=2021, grain=0.75).convert("RGBA")
    fd = ImageDraw.Draw(fc)
    rng = np.random.default_rng(777)
    for _ in range(55):
        sx = int(rng.integers(int(W * 0.45), W - 20))
        sy = int(rng.integers(40, H - 40))
        br = int(rng.integers(40, 110))
        fd.ellipse([sx, sy, sx + 1, sy + 1], fill=(182, 210, 238, br))
    fc_out = os.path.join(GUI_DIR, "flowchart_bg.webp")
    fc.convert("RGB").save(fc_out, "WEBP", quality=93, method=4)
    print(f"[OK] Built softened Frosted Mist Flowchart Backdrop: {fc_out} ({os.path.getsize(fc_out)//1024} KB)")


def build_refined_music_disc_and_icons():
    # Minimalist Frosted Obsidian Lunar Disc (matching Plan A soft silver-blue + dusty rose!)
    S = 1024
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, cy = S // 2, S // 2
    d.ellipse([24, 24, S - 24, S - 24], fill=(16, 21, 30, 255), outline=(188, 210, 234, 110), width=4)
    for rad in range(160, 470, 24):
        d.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], outline=(176, 198, 224, 20), width=2)
    d.arc([110, 110, S - 110, S - 110], start=280, end=355, fill=(162, 198, 230, 155), width=5)
    d.arc([165, 165, S - 165, S - 165], start=110, end=175, fill=(214, 154, 164, 115), width=4)
    d.ellipse([cx - 122, cy - 122, cx + 122, cy + 122], fill=(22, 28, 40, 255), outline=(210, 226, 244, 130), width=3)
    d.ellipse([cx - 88, cy - 88, cx + 88, cy + 88], outline=(162, 198, 230, 120), width=2)
    d.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], fill=(12, 16, 24, 255), outline=(224, 236, 248, 175), width=3)
    im.resize((512, 512), Image.Resampling.LANCZOS).save(os.path.join(GUI_DIR, "music_disc.png"))

    # Softened thin-stroke icons
    icons_dir = os.path.join(GUI_DIR, "icons")
    os.makedirs(icons_dir, exist_ok=True)
    L = 192
    im = Image.new("RGBA", (L, L), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    col = (164, 182, 204, 210)
    d.arc([64, 34, 128, 102], start=180, end=360, fill=col, width=8)
    d.line([(64, 68), (64, 90)], fill=col, width=8)
    d.line([(128, 68), (128, 90)], fill=col, width=8)
    d.rounded_rectangle([46, 88, 146, 162], radius=12, outline=col, width=8)
    d.ellipse([88, 114, 104, 130], fill=col)
    d.line([(96, 126), (96, 144)], fill=col, width=6)
    im.resize((44, 44), Image.Resampling.LANCZOS).save(os.path.join(icons_dir, "lock.png"))

    S = 128
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.polygon([(64, 18), (112, 106), (16, 106)], outline=(222, 146, 158, 240), width=8)
    d.line([(64, 48), (64, 78)], fill=(236, 166, 178, 255), width=8)
    d.ellipse([59, 88, 69, 98], fill=(236, 166, 178, 255))
    im.resize((28, 28), Image.Resampling.LANCZOS).save(os.path.join(icons_dir, "warn.png"))

    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = S // 2
    pts = [(c, 10), (c + 10, c - 10), (S - 10, c), (c + 10, c + 10),
           (c, S - 10), (c - 10, c + 10), (10, c), (c - 10, c - 10)]
    d.polygon(pts, fill=(228, 206, 148, 255))
    im.resize((28, 28), Image.Resampling.LANCZOS).save(os.path.join(icons_dir, "star_gold.png"))

    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(im).ellipse([24, 24, 104, 104], fill=(162, 198, 230, 235))
    im.resize((24, 24), Image.Resampling.LANCZOS).save(os.path.join(icons_dir, "heart.png"))

    # Crisp soft-mint checkmark icon used on seen choices (gui/icons/check.png)
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.line([(24, 68), (52, 96), (104, 34)], fill=(146, 207, 185, 255), width=14, joint="curve")
    im.resize((32, 32), Image.Resampling.LANCZOS).save(os.path.join(icons_dir, "check.png"))
    print("[OK] Updated Frosted Mist music disc & soft pastel icons")


def build_original_ui_audio(audio_dir=None):
    """
    Synthesize 100% original procedural Frosted Mist glass/chime UI SFX (44.1kHz 16-bit PCM WAV).
    Zero third-party audio samples — 100% open-source clean!
    """
    import wave
    out_dir = audio_dir or os.path.join(GAME, "audio")
    os.makedirs(out_dir, exist_ok=True)
    sr = 44100

    def save_wav(fname, samples):
        pcm = np.clip(samples * 32767.0, -32768, 32767).astype("<i2")
        with wave.open(os.path.join(out_dir, fname), "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sr)
            wf.writeframes(pcm.tobytes())

    # 1. ui_hover.wav: ultra-soft muted glass tick (38 ms)
    t = np.linspace(0.0, 0.038, int(sr * 0.038), endpoint=False, dtype=np.float32)
    env = np.sin(np.minimum(t / 0.004, 1.0) * (np.pi / 2.0)) * np.exp(-t * 115.0)
    sig = 0.14 * env * (0.72 * np.sin(2 * np.pi * 1180.0 * t) + 0.28 * np.sin(2 * np.pi * 2360.0 * t))
    save_wav("ui_hover.wav", sig)

    # 2. ui_click.wav: clean crisp frosted-glass confirm chime (95 ms)
    t = np.linspace(0.0, 0.095, int(sr * 0.095), endpoint=False, dtype=np.float32)
    env = np.sin(np.minimum(t / 0.003, 1.0) * (np.pi / 2.0)) * np.exp(-t * 44.0)
    sig = 0.24 * env * (
        0.65 * np.sin(2 * np.pi * 880.0 * t)
        + 0.25 * np.sin(2 * np.pi * 1318.5 * t)
        + 0.10 * np.sin(2 * np.pi * 2637.0 * t) * np.exp(-t * 40.0)
    )
    save_wav("ui_click.wav", sig)

    # 3. ui_cancel.wav: gentle descending double-tap (115 ms)
    t = np.linspace(0.0, 0.115, int(sr * 0.115), endpoint=False, dtype=np.float32)
    freq = 660.0 * np.exp(-t * 3.8)
    phase = 2.0 * np.pi * np.cumsum(freq) / sr
    env = np.sin(np.minimum(t / 0.004, 1.0) * (np.pi / 2.0)) * np.exp(-t * 36.0)
    sig = 0.22 * env * (0.78 * np.sin(phase) + 0.22 * np.sin(phase * 2.0) * np.exp(-t * 30.0))
    save_wav("ui_cancel.wav", sig)

    # 4. ui_choice.wav: crystalline lunar bell resonance (220 ms)
    t = np.linspace(0.0, 0.220, int(sr * 0.220), endpoint=False, dtype=np.float32)
    env = np.sin(np.minimum(t / 0.004, 1.0) * (np.pi / 2.0)) * np.exp(-t * 17.5)
    sig = 0.26 * env * (
        0.55 * np.sin(2 * np.pi * 783.99 * t)
        + 0.30 * np.sin(2 * np.pi * 1174.66 * t)
        + 0.15 * np.sin(2 * np.pi * 1567.98 * t) * np.exp(-t * 12.0)
    )
    save_wav("ui_choice.wav", sig)
    print(f"[OK] Synthesized 4 original open-source UI chimes in {out_dir}")


def build_original_window_icon(gui_dir=None, proj_dir=None):
    """Render a 100% original procedural Blue Glass Moon window icon (PNG + multi-size ICO)."""
    g_dir = gui_dir or GUI_DIR
    p_dir = proj_dir or os.path.join(ROOT, "Tsukihime_HD")
    S = 512
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    cx, cy = S / 2.0, S / 2.0
    r = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)

    # Deep cobalt rounded-square badge
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    bg = np.zeros((S, S, 4), dtype=np.uint8)
    ny = yy / float(S)
    nx = xx / float(S)
    bg[:, :, 0] = np.clip(14 + 28 * nx + 18 * ny, 0, 255).astype(np.uint8)
    bg[:, :, 1] = np.clip(24 + 44 * nx + 24 * ny, 0, 255).astype(np.uint8)
    bg[:, :, 2] = np.clip(68 + 78 * nx + 54 * ny, 0, 255).astype(np.uint8)
    bg[:, :, 3] = 255
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).rounded_rectangle([20, 20, S - 20, S - 20], radius=104, fill=255)
    bg_im = Image.fromarray(bg, mode="RGBA")
    bg_im.putalpha(mask)
    im.alpha_composite(bg_im)

    # Soft cyan lunar glow + crisp pale pearl full moon with subtle crescent shadow ring
    glow = np.exp(-((r / 175.0) ** 2.0))
    g_arr = np.zeros((S, S, 4), dtype=np.uint8)
    g_arr[:, :, 0] = 132
    g_arr[:, :, 1] = 198
    g_arr[:, :, 2] = 255
    g_arr[:, :, 3] = np.clip(glow * 140.0, 0, 255).astype(np.uint8)
    im.alpha_composite(Image.fromarray(g_arr, mode="RGBA"))

    disc = np.clip((132.0 - r) / 4.0, 0.0, 1.0)
    m_arr = np.zeros((S, S, 4), dtype=np.uint8)
    shade = np.clip(1.0 - 0.14 * ((xx - cx + 45.0) / 140.0) ** 2, 0.82, 1.0)
    m_arr[:, :, 0] = np.clip(234 * shade, 0, 255).astype(np.uint8)
    m_arr[:, :, 1] = np.clip(242 * shade, 0, 255).astype(np.uint8)
    m_arr[:, :, 2] = 255
    m_arr[:, :, 3] = np.clip(disc * 255.0, 0, 255).astype(np.uint8)
    im.alpha_composite(Image.fromarray(m_arr, mode="RGBA"))

    # Crisp glass rim outline
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([22, 22, S - 22, S - 22], radius=102, outline=(196, 222, 248, 95), width=6)

    icon_256 = im.resize((256, 256), Image.Resampling.LANCZOS)
    icon_256.save(os.path.join(g_dir, "window_icon.png"))
    icon_256.save(os.path.join(p_dir, "icon.ico"), format="ICO", sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
    print(f"[OK] Built original Blue Glass Moon window_icon.png & icon.ico")


def build_heroine_portrait_assets(game_dir=None):
    """
    Build 2x-supersampled soft bottom-feathered transparent heroine portraits
    (normal + high-affection expressions), pastel rounded progress bars & ending pills
    for Plan 3 Near/Far Layered Heroine Affection cards.
    NOTE: Portraits are user-derived BYOA assets generated locally from imported tachi sprites!
    """
    g_root = game_dir or GAME
    gui_dir = os.path.join(g_root, "gui")
    mist_dir = os.path.join(gui_dir, "mist")
    p_dir = os.path.join(gui_dir, "portraits")
    tachi_dir = os.path.join(g_root, "images", "tachi")
    os.makedirs(p_dir, exist_ok=True)
    os.makedirs(mist_dir, exist_ok=True)

    specs = [
        # (key, norm_tachi, warm_tachi, w, h, zoom_boost, rgb)
        ("arc",    "ark_t01a.webp",  "ark_t08.webp",  236, 288, 1.12, (222, 200, 148)),
        ("ciel",   "cel_t01a.webp",  "cel_t03.webp",  236, 288, 1.12, (152, 194, 226)),
        ("akiha",  "aki_t01a.webp",  "aki_t04a.webp", 176, 304, 1.08, (214, 152, 163)),
        ("hisui",  "his_t01.webp",   "his_t02.webp",  176, 304, 1.08, (154, 201, 207)),
        ("kohaku", "koha_t01a.webp", "koha_t03.webp", 176, 304, 1.08, (221, 182, 146)),
    ]

    def make_portrait(src_fn, tw, th, zoom_boost, dst_path):
        im = Image.open(os.path.join(tachi_dir, src_fn)).convert("RGBA")
        bbox = im.getbbox()
        if bbox:
            im = im.crop(bbox)
        scale = max(tw / float(im.width), th / float(im.height)) * zoom_boost
        nw, nh = int(im.width * scale), int(im.height * scale)
        im = im.resize((nw, nh), Image.Resampling.LANCZOS)
        cx = (nw - tw) // 2
        cropped = im.crop((cx, 0, cx + tw, th))

        # Soft bottom alpha feathering + crisp rounded corner clip (radius 14)
        arr = np.array(cropped, dtype=np.float32)
        fade_px = 38
        fade = np.ones((th,), dtype=np.float32)
        fade[th - fade_px:] = np.linspace(1.0, 0.0, fade_px, dtype=np.float32) ** 1.3
        arr[:, :, 3] *= fade[:, None]
        cropped = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), mode="RGBA")

        S = 2
        mask = Image.new("L", (tw * S, th * S), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, tw * S - 1, th * S - 1], radius=14 * S, fill=255)
        mask = mask.resize((tw, th), Image.Resampling.LANCZOS)
        a = np.minimum(np.array(cropped.getchannel("A")), np.array(mask))
        cropped.putalpha(Image.fromarray(a, mode="L"))
        cropped.save(dst_path)

    # Neutral rounded progress track (32x10)
    draw_rr_sprite(32, 10, 5, fill=(220, 234, 250, 34)).save(os.path.join(mist_dir, "prog_track.png"))

    for key, norm_fn, warm_fn, tw, th, zb, rgb in specs:
        make_portrait(norm_fn, tw, th, zb, os.path.join(p_dir, f"{key}_norm.png"))
        make_portrait(warm_fn, tw, th, zb, os.path.join(p_dir, f"{key}_warm.png"))
        # Soft dark-mist portrait backing frame tinted delicately with route pastel
        draw_rr_sprite(96, 96, 16, fill=(14, 20, 30, 196), outline=(*rgb, 78), outline_w=1).save(os.path.join(mist_dir, f"pbox_{key}.png"))
        # Pastel rounded progress bar fill (32x10)
        draw_rr_sprite(32, 10, 5, fill=(*rgb, 235)).save(os.path.join(mist_dir, f"prog_{key}.png"))
        # Cleared ending pastel capsule pill (80x36)
        draw_rr_sprite(80, 36, 18, fill=(*rgb, 48), outline=(*rgb, 138), outline_w=1).save(os.path.join(mist_dir, f"epill_{key}.png"))

    print(f"[OK] Built 10 feathered heroine portraits (normal + warm) in {p_dir}")


def _periodic_fft_noise(w, h, beta=3.2, min_freq=2.0, max_freq=52.0, seed=42):
    """Generate a mathematically X-periodic ultra-smooth 2D fBM field via 2D FFT (zero swirl artifacts)."""
    rng = np.random.default_rng(seed)
    fy = np.fft.fftfreq(h)[:, None] * h
    fx = np.fft.rfftfreq(w)[None, :] * w
    dist = np.sqrt((fx * (h / float(w))) ** 2 + fy ** 2)
    amp = np.zeros_like(dist, dtype=np.float32)
    valid = (dist >= min_freq) & (dist <= max_freq)
    amp[valid] = 1.0 / (dist[valid] ** (beta * 0.5))
    amp *= np.exp(-((dist / (max_freq * 0.80)) ** 4))
    phase = rng.uniform(0.0, 2.0 * np.pi, size=dist.shape)
    spec = amp * (np.cos(phase) + 1j * np.sin(phase))
    spec[0, 0] = 0.0
    field = np.fft.irfft2(spec, s=(h, w)).astype(np.float32)
    std = float(field.std()) + 1e-6
    return (field - float(field.mean())) / std


def _render_volumetric_cloud_strip(w, h, seed, palette, mode="cumulus",
                                   max_alpha=245, light_step=(13, -18),
                                   optical_k=1.35):
    """
    Synthesize a horizontally seamless (C-infinity periodic in X) anime-grade
    volumetric cumulus or wispy cloud strip using overlapping multi-scale soft
    cloud billows + smooth high-beta fBM cotton erosion + Beer-Lambert raymarched
    moonlight transmittance (zero marble swirls, zero seams!).
    """
    rng = np.random.default_rng(seed)
    # Build cloud density at half resolution (960 x h/2) for buttery-fast speed & silky softness, then upsample!
    sw, sh = w // 2, h // 2
    yy, xx = np.mgrid[0:sh, 0:sw].astype(np.float32)
    dens = np.zeros((sh, sw), dtype=np.float32)

    if mode == "cumulus":
        # 1. Clustered billowing cumulus towers along a dramatic wavy horizon silhouette (periodic in sw!)
        n_towers = 15
        tower_xs = np.linspace(0, sw, n_towers, endpoint=False) + rng.uniform(-24, 24, size=n_towers)
        # Create tall billowing cloud peaks and graceful valleys so the full moon shines boldly above!
        wave = np.sin(np.linspace(0, 4.0 * np.pi, n_towers, endpoint=False) + 0.6)
        tower_ys = sh * (0.46 + 0.16 * wave + rng.uniform(-0.06, 0.06, size=n_towers))
        puffs = []
        for tx, ty in zip(tower_xs, tower_ys):
            # Main wide body puff
            puffs.append((tx % sw, ty + rng.uniform(24, 58), rng.uniform(90, 145), rng.uniform(58, 96), rng.uniform(0.55, 0.85)))
            # Crown cauliflower puffs
            for _ in range(rng.integers(6, 10)):
                px = (tx + rng.normal(0, 56)) % sw
                py = ty + rng.normal(-12, 30)
                rx = rng.uniform(34, 78)
                ry = rx * rng.uniform(0.66, 0.90)
                puffs.append((px, py, rx, ry, rng.uniform(0.42, 0.78)))
            # Delicate cotton rim tufts
            for _ in range(rng.integers(5, 9)):
                px = (tx + rng.normal(0, 74)) % sw
                py = ty + rng.normal(-24, 34)
                rx = rng.uniform(18, 40)
                ry = rx * rng.uniform(0.65, 0.90)
                puffs.append((px, py, rx, ry, rng.uniform(0.28, 0.56)))
        # Secondary sculpted lower billows (keeps bottom richly dimensional instead of flat purple!)
        for bx in np.linspace(0, sw, 18, endpoint=False):
            puffs.append(((bx + rng.uniform(-20, 20)) % sw, sh * rng.uniform(0.84, 1.06), rng.uniform(86, 140), rng.uniform(48, 78), rng.uniform(0.55, 0.82)))

    elif mode == "high":
        # Sparse, delicate floating cotton cumulus tufts in the upper sky (like Tsukihime R!)
        puffs = []
        n_clusters = 8
        c_xs = np.linspace(0, sw, n_clusters, endpoint=False) + rng.uniform(-35, 35, size=n_clusters)
        for cx in c_xs:
            cy = sh * rng.uniform(0.18, 0.66)
            for _ in range(rng.integers(5, 10)):
                px = (cx + rng.normal(0, 54)) % sw
                py = cy + rng.normal(0, 22)
                rx = rng.uniform(28, 72)
                ry = rx * rng.uniform(0.42, 0.68)
                puffs.append((px, py, rx, ry, rng.uniform(0.32, 0.62)))

    else:  # "near" - silky translucent mist banks gliding gently across the bottom
        puffs = []
        n_banks = 12
        b_xs = np.linspace(0, sw, n_banks, endpoint=False) + rng.uniform(-30, 30, size=n_banks)
        for bx in b_xs:
            by = sh * rng.uniform(0.46, 0.90)
            for _ in range(rng.integers(4, 8)):
                px = (bx + rng.normal(0, 68)) % sw
                py = by + rng.normal(0, 26)
                rx = rng.uniform(55, 125)
                ry = rx * rng.uniform(0.38, 0.60)
                puffs.append((px, py, rx, ry, rng.uniform(0.28, 0.52)))

    # Accumulate soft metaball puffs with exact toroidal X distance!
    for px, py, rx, ry, wt in puffs:
        dx = np.abs(xx - px)
        dx = np.minimum(dx, sw - dx)
        dy = yy - py
        r2 = (dx / rx) ** 2 + (dy / ry) ** 2
        # Compact smooth falloff (C2 continuous, zero hard edges)
        g = np.clip(1.0 - r2 * 0.52, 0.0, 1.0)
        dens += (g * g * g) * wt

    # Organic cottony edge modulation using smooth un-warped high-beta periodic fBM
    fbm_lo = _periodic_fft_noise(sw, sh, beta=3.2, min_freq=2.0, max_freq=28.0, seed=seed + 11)
    fbm_hi = _periodic_fft_noise(sw, sh, beta=2.7, min_freq=8.0, max_freq=64.0, seed=seed + 29)
    cotton = fbm_lo * 0.24 + fbm_hi * 0.10

    if mode == "cumulus":
        raw = dens + cotton * (0.28 + 0.42 * np.clip(dens, 0.0, 1.0)) - 0.34
        alpha_f = np.clip(raw / 0.58, 0.0, 1.0)
        # Soft top boundary fade so strip top never clips
        ny = np.linspace(0.0, 1.0, sh, dtype=np.float32)[:, None]
        top_env = np.clip(ny / 0.16, 0.0, 1.0)
        alpha_f *= top_env * top_env * (3.0 - 2.0 * top_env)
    elif mode == "high":
        raw = dens + cotton * 0.24 - 0.36
        alpha_f = np.clip(raw / 0.55, 0.0, 1.0)
        ny = np.linspace(0.0, 1.0, sh, dtype=np.float32)[:, None]
        env = np.clip(ny / 0.14, 0.0, 1.0) * np.clip((1.0 - ny) / 0.28, 0.0, 1.0)
        alpha_f *= env * env * (3.0 - 2.0 * env)
    else:
        raw = dens + cotton * 0.26 - 0.30
        alpha_f = np.clip(raw / 0.62, 0.0, 1.0)
        ny = np.linspace(0.0, 1.0, sh, dtype=np.float32)[:, None]
        top_env = np.clip(ny / 0.30, 0.0, 1.0)
        alpha_f *= top_env * top_env * (3.0 - 2.0 * top_env)

    # Smooth volumetric density for Beer-Lambert raymarching toward the Moon
    vol_d = np.clip(alpha_f * (0.65 + 0.55 * np.clip(dens, 0.0, 1.6)), 0.0, 1.8)
    # 18 fine Beer-Lambert optical depth steps (zero step-echo artifacts!)
    ldx, ldy = light_step
    opt_depth = np.zeros_like(vol_d)
    for step_i in range(1, 19):
        swt = 0.14 * (0.90 ** (step_i - 1))
        ox = int(round(ldx * step_i * 0.28))
        oy = int(round(ldy * step_i * 0.28))
        shifted_x = np.roll(vol_d, -ox, axis=1)
        shifted = np.zeros_like(vol_d)
        if oy < 0:
            k = -oy
            if k < sh:
                shifted[k:, :] = shifted_x[:sh - k, :]
        elif oy > 0:
            k = oy
            if k < sh:
                shifted[:sh - k, :] = shifted_x[k:, :]
        else:
            shifted = shifted_x
        opt_depth += shifted * swt

    # Periodic horizontal smooth blur on optical depth for buttery painterly scattering
    pad_b = 12
    od_pad = np.concatenate([opt_depth[:, -pad_b:], opt_depth, opt_depth[:, :pad_b]], axis=1)
    od_max = max(float(od_pad.max()), 1e-4)
    od_sm = np.array(
        Image.fromarray(np.clip((od_pad / od_max) * 255.0, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(radius=3.5)),
        dtype=np.float32,
    ) * (od_max / 255.0)
    opt_depth = od_sm[:, pad_b:-pad_b]

    # Beer-Lambert transmittance + internal puffy multiple-scattering variation
    trans = np.exp(-opt_depth * optical_k)
    ny_l = np.linspace(0.0, 1.0, sh, dtype=np.float32)[:, None]
    edge_glow = np.clip(1.0 - vol_d * 0.72, 0.0, 1.0) * np.clip(1.0 - ny_l * 0.75, 0.0, 1.0) * 0.28
    # Internal volumetric billow highlights inside mid/lower cloud sea
    inner_sculpt = np.clip(fbm_lo * 0.55 + 0.5, 0.0, 1.0) * (0.20 + 0.18 * (1.0 - trans)) * np.clip(dens * 0.65, 0.0, 1.0)
    lit = np.clip(trans * 0.86 + edge_glow + inner_sculpt, 0.0, 1.0)
    lit = np.clip(lit ** 0.84, 0.0, 1.0)

    # 4-stop painterly color ramp (deep indigo shadow -> royal violet -> luminous orchid -> pearl sunlit white)
    c0, c1, c2, c3 = [np.array(c, dtype=np.float32) for c in palette]
    rgb = np.zeros((sh, sw, 3), dtype=np.float32)
    s1 = np.clip(lit / 0.36, 0.0, 1.0)
    s2 = np.clip((lit - 0.36) / 0.36, 0.0, 1.0)
    s3 = np.clip((lit - 0.72) / 0.28, 0.0, 1.0)
    for ch in range(3):
        v = c0[ch] * (1.0 - s1) + c1[ch] * s1
        v = v * (1.0 - s2) + c2[ch] * s2
        v = v * (1.0 - s3) + c3[ch] * s3
        rgb[:, :, ch] = v

    rgba_half = np.zeros((sh, sw, 4), dtype=np.uint8)
    rgba_half[:, :, :3] = np.clip(rgb, 0, 255).astype(np.uint8)
    rgba_half[:, :, 3] = np.clip((alpha_f ** 0.92) * max_alpha, 0, 255).astype(np.uint8)
    im_half = Image.fromarray(rgba_half, mode="RGBA")
    # Upsample smoothly to full 1920px width (zero pixelation, dreamy painterly cloud edges!)
    im_full = im_half.resize((w, h), Image.Resampling.BICUBIC)
    return im_full


def build_user_derived_title_art(title1_img, out_gui_dir=None):
    """
    BYOA User-Derived Title Art Synthesizer (runs locally from user's own title1.jpg!).
    Generates from original 640x480 title1.jpg (or existing main_menu.webp):
      1. gui/main_menu.webp           - Option B Asymmetric serene midnight-blue full moon + authentic deep-ink `月姫`
      2. gui/title_eclipse_moon.png   - Standalone radiant pearl full moon + ice-cyan halo (960x960 at 850,16)
      3. gui/title_eclipse_kanji.png  - Crisp white-filled, deep-indigo-outlined `月姫` calligraphy (360x670 at 1150,160)
    """
    g_dir = out_gui_dir or GUI_DIR
    os.makedirs(g_dir, exist_ok=True)
    W, H = 1920, 1080
    MCX, MCY, MR = 1330.5, 495.5, 346.0

    # Normalize source: accept PIL.Image of 640x480 original title1.jpg
    src = title1_img.convert("RGB")
    sw, sh = src.size
    # Original title1.jpg (640x480) has centered moon (cx≈320, cy≈240, r≈206) and deep-ink `月姫` above y=322
    # Upscale source cleanly to high-res working plate (2560x1920 = 4x)
    up_w, up_h = 2560, 1920
    up = src.resize((up_w, up_h), Image.Resampling.LANCZOS)
    up_arr = np.array(up, dtype=np.float32)
    up_lum = 0.299 * up_arr[:, :, 0] + 0.587 * up_arr[:, :, 1] + 0.114 * up_arr[:, :, 2]

    # Detect exact moon center & radius strictly inside upper-central sky (avoids lower-left/right clouds!)
    uy, ux = np.mgrid[0:up_h, 0:up_w].astype(np.float32)
    upper_bright = (up_lum > 180) & (uy < up_h * 0.52) & (ux > up_w * 0.14) & (ux < up_w * 0.86)
    ys_b, xs_b = np.where(upper_bright)
    if len(xs_b) > 1000:
        src_cx = float(xs_b.min() + xs_b.max()) / 2.0
        src_r = float(xs_b.max() - xs_b.min()) / 2.0
        src_cy = float(ys_b.min()) + src_r
    else:
        src_cx, src_cy, src_r = up_w * 0.4992, up_h * 0.5115, up_w * 0.3211

    udist = np.sqrt((ux - src_cx) ** 2 + (uy - src_cy) ** 2)

    # 1. Extract crisp `月姫` deep-ink calligraphy strictly INSIDE the central moon column
    k_zone = (
        (np.abs(ux - src_cx) <= src_r * 0.25)
        & (uy >= src_cy - src_r * 0.945)
        & (uy <= up_h * 0.672)
        & (udist < src_r * 0.955)
    )
    k_raw = np.where(k_zone, np.clip((155.0 - up_lum) / 110.0, 0.0, 1.0), 0.0).astype(np.float32)
    ky_idx, kx_idx = np.where(k_raw > 0.35)
    if len(kx_idx) > 200:
        k_crop_raw = k_raw[ky_idx.min():ky_idx.max() + 1, kx_idx.min():kx_idx.max() + 1]
    else:
        k_crop_raw = np.zeros((100, 50), dtype=np.float32)

    # Fit calligraphy smoothly inside target 1920x1080 moon (height ~556px centered on MCX, MCY)
    target_kh = 556
    target_kw = max(20, int(round(target_kh * (k_crop_raw.shape[1] / max(1.0, float(k_crop_raw.shape[0]))))))
    k_im_s = Image.fromarray(np.clip(k_crop_raw * 255.0, 0, 255).astype(np.uint8), mode="L").resize(
        (target_kw, target_kh), Image.Resampling.LANCZOS
    )
    kanji_full = np.zeros((H, W), dtype=np.float32)
    kx_left = int(round(MCX - target_kw / 2.0))
    ky_top = int(round(MCY - target_kh / 2.0 + 4))
    kanji_full[ky_top:ky_top + target_kh, kx_left:kx_left + target_kw] = np.clip(
        (np.array(k_im_s, dtype=np.float32) / 255.0 - 0.06) / 0.88, 0.0, 1.0
    )

    # 2. FIRST heal ALL kanji strokes out of the upper moon disc with wide normalized convolution,
    #    THEN mirror the 100%-clean upper lunar mare down over the bottom epigraph/button area!
    healed_up = up_arr.copy()
    k_heal_seed = (
        (np.abs(ux - src_cx) <= src_r * 0.27)
        & (uy <= up_h * 0.68)
        & (udist < src_r * 0.99)
        & (up_lum < 185.0)
    )
    d_w, d_h = up_w // 4, up_h // 4
    k_heal_mask = np.array(
        Image.fromarray((k_heal_seed.astype(np.uint8) * 255)).resize((d_w, d_h), Image.Resampling.BILINEAR)
        .filter(ImageFilter.MaxFilter(7)).filter(ImageFilter.GaussianBlur(radius=3.5))
        .resize((up_w, up_h), Image.Resampling.BICUBIC),
        dtype=np.float32,
    ) / 255.0
    k_heal_mask = np.clip(k_heal_mask * 1.45, 0.0, 1.0)

    valid_w2 = ((k_heal_mask < 0.08) & (uy < up_h * 0.66) & (udist < src_r * 0.975)).astype(np.float32)
    vw_sm = np.array(
        Image.fromarray((valid_w2 * 255.0).astype(np.uint8)).resize((d_w, d_h), Image.Resampling.BILINEAR)
        .filter(ImageFilter.GaussianBlur(radius=28)),
        dtype=np.float32,
    ) / 255.0
    fallback_moon = np.array([236.0, 232.0, 246.0], dtype=np.float32)
    conf = np.clip(vw_sm / 0.15, 0.0, 1.0)
    for ch in range(3):
        ch_sm = np.array(
            Image.fromarray(np.clip(up_arr[:, :, ch] * valid_w2, 0, 255).astype(np.uint8))
            .resize((d_w, d_h), Image.Resampling.BILINEAR).filter(ImageFilter.GaussianBlur(radius=28)),
            dtype=np.float32,
        )
        est = np.clip(ch_sm / np.maximum(vw_sm, 0.05), 0.0, 255.0)
        est = est * conf + fallback_moon[ch] * (1.0 - conf)
        fill_full = np.array(
            Image.fromarray(np.clip(est, 0, 255).astype(np.uint8)).resize((up_w, up_h), Image.Resampling.BICUBIC),
            dtype=np.float32,
        )
        healed_up[:, :, ch] = healed_up[:, :, ch] * (1.0 - k_heal_mask) + fill_full * k_heal_mask

    # Now mirror the 100%-kanji-free upper lunar mare into the lower text region (y > 0.655*up_h)
    mirror_y = np.clip((2.0 * src_cy - uy).astype(np.int32), 0, up_h - 1)
    bot_mask = (uy > up_h * 0.645) & (udist < src_r * 1.03)
    bot_blend = np.clip((uy - up_h * 0.645) / (up_h * 0.04), 0.0, 1.0)
    healed_copy = healed_up.copy()
    for ch in range(3):
        mirrored = healed_copy[mirror_y, np.arange(up_w)[None, :], ch]
        healed_up[:, :, ch] = np.where(bot_mask, healed_up[:, :, ch] * (1.0 - bot_blend) + mirrored * bot_blend, healed_up[:, :, ch])

    # Crop moon square from healed_up and resize to exact target diameter (2*MR)
    box_r = int(round(src_r * 1.04))
    cx_i, cy_i = int(round(src_cx)), int(round(src_cy))
    pad_m = np.zeros((box_r * 2, box_r * 2, 3), dtype=np.float32)
    pad_m[:, :] = np.array([232.0, 236.0, 248.0], dtype=np.float32)
    y0s, y1s = max(0, cy_i - box_r), min(up_h, cy_i + box_r)
    x0s, x1s = max(0, cx_i - box_r), min(up_w, cx_i + box_r)
    pad_m[y0s - (cy_i - box_r):y1s - (cy_i - box_r), x0s - (cx_i - box_r):x1s - (cx_i - box_r)] = healed_up[y0s:y1s, x0s:x1s]

    target_box = int(round(MR * 2.08))
    moon_sq = np.array(
        Image.fromarray(np.clip(pad_m, 0, 255).astype(np.uint8), mode="RGB").resize((target_box, target_box), Image.Resampling.LANCZOS),
        dtype=np.float32,
    )

    # Paste clean moon into full 1920x1080 buffer centered on (MCX, MCY)
    moon_canvas = np.full((H, W, 3), 235.0, dtype=np.float32)
    mx_l = int(round(MCX - target_box / 2.0))
    my_t = int(round(MCY - target_box / 2.0))
    moon_canvas[my_t:my_t + target_box, mx_l:mx_l + target_box] = moon_sq

    # --- 3. Synthesize Default Serene Midnight-Blue Title Screen (gui/main_menu.webp) ---
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    nx, ny = xx / float(W), yy / float(H)
    mdist = np.sqrt((xx - MCX) ** 2 + (yy - MCY) ** 2)

    serene = np.zeros((H, W, 3), dtype=np.float32)
    s_tl = np.array([4.0, 7.0, 15.0], dtype=np.float32)
    s_tr = np.array([20.0, 42.0, 96.0], dtype=np.float32)
    s_bl = np.array([7.0, 11.0, 24.0], dtype=np.float32)
    s_br = np.array([26.0, 50.0, 108.0], dtype=np.float32)
    for ch in range(3):
        t_row = s_tl[ch] * (1.0 - nx) + s_tr[ch] * nx
        b_row = s_bl[ch] * (1.0 - nx) + s_br[ch] * nx
        serene[:, :, ch] = t_row * (1.0 - ny) + b_row * ny

    # Soft cool lunar halo & subtle lower mist
    cool_glow = np.exp(-((mdist / 520.0) ** 1.9))
    serene[:, :, 0] += 18.0 * cool_glow
    serene[:, :, 1] += 36.0 * cool_glow
    serene[:, :, 2] += 78.0 * cool_glow
    disc_a = np.clip((MR + 2.5 - mdist) / 8.0, 0.0, 1.0)
    disc_a = disc_a * disc_a * (3.0 - 2.0 * disc_a)
    for ch in range(3):
        serene[:, :, ch] = serene[:, :, ch] * (1.0 - disc_a) + moon_canvas[:, :, ch] * disc_a

    # Composite crisp deep-ink `月姫` calligraphy onto default serene moon
    ink_col = np.array([10.0, 18.0, 34.0], dtype=np.float32)
    for ch in range(3):
        serene[:, :, ch] = serene[:, :, ch] * (1.0 - kanji_full) + ink_col[ch] * kanji_full

    rng = np.random.default_rng(2000)
    serene += rng.normal(0.0, 0.7, size=(H, W, 3)).astype(np.float32)
    ser_im = Image.fromarray(np.clip(serene, 0, 255).astype(np.uint8), mode="RGB").convert("RGBA")
    sd = ImageDraw.Draw(ser_im)
    for _ in range(75):
        sx_i = int(rng.integers(240, W - 40))
        sy_i = int(rng.integers(24, int(H * 0.65)))
        if ((sx_i - MCX) ** 2 + (sy_i - MCY) ** 2) < (MR + 45) ** 2:
            continue
        br = int(rng.integers(60, 165))
        sd.ellipse([sx_i, sy_i, sx_i + 1, sy_i + 1], fill=(208, 224, 248, br))
    mm_out = os.path.join(g_dir, "main_menu.webp")
    ser_im.convert("RGB").save(mm_out, "WEBP", quality=94, method=4)

    # --- 4. Synthesize Eclipse White-Outlined `月姫` Calligraphy (gui/title_eclipse_kanji.png) ---
    kx0, ky0, kx1, ky1 = 1150, 160, 1510, 830
    k_crop = kanji_full[ky0:ky1, kx0:kx1]
    kw, kh = kx1 - kx0, ky1 - ky0
    k_mask_im = Image.fromarray(np.clip(k_crop * 255.0, 0, 255).astype(np.uint8), mode="L")
    stroke_l = k_mask_im.filter(ImageFilter.MaxFilter(7)).filter(ImageFilter.GaussianBlur(radius=0.8))
    stroke_arr = np.clip(np.array(stroke_l, dtype=np.float32) / 210.0, 0.0, 1.0)
    glow_l = k_mask_im.filter(ImageFilter.MaxFilter(11)).filter(ImageFilter.GaussianBlur(radius=8.5))
    glow_arr = np.clip(np.array(glow_l, dtype=np.float32) / 255.0, 0.0, 1.0) * 0.62

    g_col = np.array([128.0, 184.0, 255.0], dtype=np.float32)
    s_col = np.array([24.0, 32.0, 96.0], dtype=np.float32)
    f_col = np.array([253.0, 254.0, 255.0], dtype=np.float32)
    a_out = glow_arr
    c_out = np.broadcast_to(g_col, (kh, kw, 3)).copy()
    inv_sa = 1.0 - stroke_arr
    new_a = stroke_arr + a_out * inv_sa
    for ch in range(3):
        c_out[:, :, ch] = (s_col[ch] * stroke_arr + c_out[:, :, ch] * a_out * inv_sa) / np.maximum(new_a, 1e-5)
    a_out = new_a
    inv_fa = 1.0 - k_crop
    new_a = k_crop + a_out * inv_fa
    for ch in range(3):
        c_out[:, :, ch] = (f_col[ch] * k_crop + c_out[:, :, ch] * a_out * inv_fa) / np.maximum(new_a, 1e-5)
    a_out = new_a
    k_rgba = np.zeros((kh, kw, 4), dtype=np.uint8)
    k_rgba[:, :, :3] = np.clip(c_out, 0, 255).astype(np.uint8)
    k_rgba[:, :, 3] = np.clip(a_out * 255.0, 0, 255).astype(np.uint8)
    Image.fromarray(k_rgba, mode="RGBA").save(os.path.join(g_dir, "title_eclipse_kanji.png"))

    # --- 5. Synthesize Standalone Eclipse Full Moon Layer (gui/title_eclipse_moon.png, 960x960 at 850,16) ---
    CW = 960
    mx0, my0 = 850, 16
    moon_patch = np.zeros((CW, CW, 3), dtype=np.float32)
    sy0, sy1 = max(0, my0), min(H, my0 + CW)
    sx0, sx1 = max(0, mx0), min(W, mx0 + CW)
    moon_patch[sy0 - my0:sy1 - my0, sx0 - mx0:sx1 - mx0] = moon_canvas[sy0:sy1, sx0:sx1]

    cyy, cxx = np.mgrid[0:CW, 0:CW].astype(np.float32)
    cdist = np.sqrt((cxx - CW / 2.0) ** 2 + (cyy - CW / 2.0) ** 2)
    m_rgb = np.zeros((CW, CW, 3), dtype=np.float32)
    m_rgb[:, :, 0] = np.clip(moon_patch[:, :, 0] * 0.78 + 64.0, 0, 255)
    m_rgb[:, :, 1] = np.clip(moon_patch[:, :, 1] * 0.78 + 66.0, 0, 255)
    m_rgb[:, :, 2] = np.clip(moon_patch[:, :, 2] * 0.84 + 54.0, 0, 255)
    core_l = np.exp(-((cdist / (MR * 0.96)) ** 2.1))
    m_rgb[:, :, 0] = np.clip(m_rgb[:, :, 0] + 24.0 * core_l, 0, 255)
    m_rgb[:, :, 1] = np.clip(m_rgb[:, :, 1] + 26.0 * core_l, 0, 255)
    m_rgb[:, :, 2] = np.clip(m_rgb[:, :, 2] + 28.0 * core_l, 0, 255)

    disc_c = np.clip((MR + 3.0 - cdist) / 10.0, 0.0, 1.0)
    disc_c = disc_c * disc_c * (3.0 - 2.0 * disc_c)
    halo_a = np.exp(-((np.maximum(0.0, cdist - MR * 0.94) / 88.0) ** 1.65)) * 0.82
    halo_a *= np.clip((CW / 2.0 - cdist) / 60.0, 0.0, 1.0)
    tot_a = np.maximum(disc_c, halo_a)

    t_h = np.clip((cdist - MR * 0.92) / 130.0, 0.0, 1.0)
    h_rgb = np.zeros((CW, CW, 3), dtype=np.float32)
    h_rgb[:, :, 0] = 178.0 * (1.0 - t_h) + 124.0 * t_h
    h_rgb[:, :, 1] = 236.0 * (1.0 - t_h) + 168.0 * t_h
    h_rgb[:, :, 2] = 255.0

    moon_rgba = np.zeros((CW, CW, 4), dtype=np.uint8)
    for ch in range(3):
        moon_rgba[:, :, ch] = np.clip(h_rgb[:, :, ch] * (1.0 - disc_c) + m_rgb[:, :, ch] * disc_c, 0, 255).astype(np.uint8)
    moon_rgba[:, :, 3] = np.clip(tot_a * 255.0, 0, 255).astype(np.uint8)
    Image.fromarray(moon_rgba, mode="RGBA").save(os.path.join(g_dir, "title_eclipse_moon.png"))

    print(f"[OK] Synthesized BYOA user-derived title art (main_menu.webp + eclipse moon & kanji) in {g_dir}")


def build_eclipse_sky_and_clouds(out_gui_dir=None):
    """
    Build 100% original procedural Eclipse sky, breathing lunar corona, 3 seamless
    Beer-Lambert volumetric cloud layers, left readability veil & sapphire crystal shards.
    Contains ZERO copyrighted artwork — safe to track directly in open-source Git!
    """
    g_dir = out_gui_dir or GUI_DIR
    os.makedirs(g_dir, exist_ok=True)
    W, H = 1920, 1080
    MCX, MCY, MR = 1330.5, 495.5, 346.0
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    nx = xx / float(W)
    ny = yy / float(H)
    mdist = np.sqrt((xx - MCX) ** 2 + (yy - MCY) ** 2)

    # --- A. Pure Saturated Royal Cobalt-Indigo -> Violet Twilight Sky ---
    sky = np.zeros((H, W, 3), dtype=np.float32)
    c_tl = np.array([10.0, 14.0, 56.0], dtype=np.float32)
    c_tr = np.array([14.0, 48.0, 206.0], dtype=np.float32)
    c_bl = np.array([34.0, 20.0, 94.0], dtype=np.float32)
    c_br = np.array([86.0, 48.0, 184.0], dtype=np.float32)

    sx = nx ** 0.82
    sy = ny ** 1.02
    for ch in range(3):
        top_c = c_tl[ch] * (1.0 - sx) + c_tr[ch] * sx
        bot_c = c_bl[ch] * (1.0 - sx) + c_br[ch] * sx
        sky[:, :, ch] = top_c * (1.0 - sy) + bot_c * sy

    sky_glow = np.exp(-((mdist / 590.0) ** 1.80))
    sky[:, :, 0] += 34.0 * sky_glow
    sky[:, :, 1] += 88.0 * sky_glow
    sky[:, :, 2] += 146.0 * sky_glow

    vgx, vgy = 0.48 * W, 0.84 * H
    vdist = np.sqrt(((xx - vgx) / (W * 0.56)) ** 2 + ((yy - vgy) / (H * 0.44)) ** 2)
    vg = np.exp(-(vdist ** 2))
    sky[:, :, 0] += 84.0 * vg
    sky[:, :, 1] += 28.0 * vg
    sky[:, :, 2] += 118.0 * vg

    rng = np.random.default_rng(200012)
    sky += rng.normal(0.0, 0.75, size=(H, W, 3)).astype(np.float32)
    sky_im = Image.fromarray(np.clip(sky, 0, 255).astype(np.uint8), mode="RGB").convert("RGBA")
    sd = ImageDraw.Draw(sky_im)
    for _ in range(95):
        sx_i = int(rng.integers(40, W - 40))
        sy_i = int(rng.integers(24, int(H * 0.68)))
        if ((sx_i - MCX) ** 2 + (sy_i - MCY) ** 2) < (MR + 55) ** 2:
            continue
        br = int(rng.integers(80, 210))
        r_s = 1 if rng.random() < 0.78 else 2
        tint = (234, 226, 255, br) if rng.random() < 0.65 else (196, 232, 255, br)
        sd.ellipse([sx_i, sy_i, sx_i + r_s, sy_i + r_s], fill=tint)

    ecl_out = os.path.join(g_dir, "main_menu_eclipse_sky.webp")
    sky_im.convert("RGB").save(ecl_out, "WEBP", quality=94, method=4)

    # --- B. Breathing Additive Lunar Corona Glow (960x960) ---
    CW = 960
    cyy, cxx = np.mgrid[0:CW, 0:CW].astype(np.float32)
    cdist = np.sqrt((cxx - CW / 2.0) ** 2 + (cyy - CW / 2.0) ** 2)
    ring = np.exp(-(((cdist - MR * 0.97) / 66.0) ** 2)) * 0.85 + np.exp(-((cdist / 420.0) ** 2.2)) * 0.42
    ring *= np.clip((CW / 2.0 - cdist) / 68.0, 0.0, 1.0)
    cor = np.zeros((CW, CW, 4), dtype=np.uint8)
    t_outer = np.clip((cdist - MR * 0.85) / 170.0, 0.0, 1.0)
    cor[:, :, 0] = np.clip(140.0 * (1.0 - t_outer) + 158.0 * t_outer, 0, 255).astype(np.uint8)
    cor[:, :, 1] = np.clip(220.0 * (1.0 - t_outer) + 116.0 * t_outer, 0, 255).astype(np.uint8)
    cor[:, :, 2] = 255
    cor[:, :, 3] = np.clip(ring * 145.0, 0, 255).astype(np.uint8)
    Image.fromarray(cor, mode="RGBA").save(os.path.join(g_dir, "title_eclipse_corona.png"))

    # --- C. Three Horizontally Seamless Volumetric Beer-Lambert Cloud Layers ---
    cloud_high = _render_volumetric_cloud_strip(
        1920, 440, seed=108, mode="high",
        palette=((54, 48, 168), (138, 114, 232), (222, 206, 255), (254, 250, 255)),
        max_alpha=178, light_step=(10, 12), optical_k=0.95,
    )
    cloud_high.save(os.path.join(g_dir, "title_cloud_high.png"))

    cloud_far = _render_volumetric_cloud_strip(
        1920, 560, seed=2026, mode="cumulus",
        palette=((44, 28, 136), (130, 74, 218), (228, 178, 254), (255, 246, 255)),
        max_alpha=246, light_step=(12, -16), optical_k=1.28,
    )
    cloud_far.save(os.path.join(g_dir, "title_cloud_far.png"))

    cloud_near = _render_volumetric_cloud_strip(
        1920, 430, seed=7741, mode="near",
        palette=((54, 34, 152), (148, 90, 228), (236, 198, 255), (255, 250, 255)),
        max_alpha=158, light_step=(10, -14), optical_k=1.05,
    )
    cloud_near.save(os.path.join(g_dir, "title_cloud_near.png"))

    # --- D. Velvet-Indigo Left Menu Readability Veil ---
    vw = 780
    veil = np.zeros((H, vw, 4), dtype=np.uint8)
    vx = np.linspace(0.0, 1.0, vw, dtype=np.float32)[None, :]
    vy = np.linspace(0.0, 1.0, H, dtype=np.float32)[:, None]
    tx = np.clip((vx - 0.18) / 0.82, 0.0, 1.0)
    hx = 1.0 - (tx * tx * (3.0 - 2.0 * tx))
    lower_boost = 0.78 + 0.22 * np.clip((vy - 0.35) / 0.55, 0.0, 1.0)
    veil[:, :, 0] = 14
    veil[:, :, 1] = 10
    veil[:, :, 2] = 44
    veil[:, :, 3] = np.clip(hx * lower_boost * 218.0, 0, 255).astype(np.uint8)
    Image.fromarray(veil, mode="RGBA").save(os.path.join(g_dir, "title_eclipse_left_veil.png"))

    # --- E. Crisp Floating Sapphire-Cyan & Silver Diamond Shards ---
    def make_motes(seed, count, fname):
        S = 2
        mw, mh = 1040, 880
        m_im = Image.new("RGBA", (mw * S, mh * S), (0, 0, 0, 0))
        md = ImageDraw.Draw(m_im)
        mrng = np.random.default_rng(seed)
        for _ in range(count):
            if mrng.random() < 0.78:
                mx = int(mrng.normal(520, 145))
                my = int(mrng.normal(560, 160))
            else:
                mx = int(mrng.integers(80, mw - 80))
                my = int(mrng.integers(80, mh - 80))
            mx = max(24, min(mw - 24, mx))
            my = max(24, min(mh - 24, my))
            sz = float(mrng.uniform(5.0, 13.0))
            ratio = float(mrng.uniform(0.24, 0.38))
            br = int(mrng.integers(155, 250))
            pts = [
                (mx * S, (my - sz) * S),
                ((mx + sz * ratio) * S, my * S),
                (mx * S, (my + sz) * S),
                ((mx - sz * ratio) * S, my * S),
            ]
            if mrng.random() < 0.58:
                col = (56, 178, 255, br)
            elif mrng.random() < 0.82:
                col = (210, 236, 255, br)
            else:
                col = (196, 152, 255, br)
            md.polygon(pts, fill=col)
        sharp = m_im.resize((mw, mh), Image.Resampling.LANCZOS)
        bloom = sharp.filter(ImageFilter.GaussianBlur(radius=2.5))
        Image.alpha_composite(bloom, sharp).save(os.path.join(g_dir, fname))

    make_motes(3141, 32, "title_motes_a.png")
    make_motes(2718, 24, "title_motes_b.png")
    print(f"[OK] Built original procedural Eclipse sky, corona, 3 seamless clouds & motes in {g_dir}")


def main():
    bundle_fonts()
    build_frosted_mist_sprites()
    build_silky_inner_backdrops()
    build_refined_music_disc_and_icons()
    build_original_ui_audio()
    build_original_window_icon()
    build_eclipse_sky_and_clouds()
    print("=== Open-Source Frosted Mist UI Asset Build Complete (Zero Copyrighted Assets) ===")


if __name__ == "__main__":
    main()
