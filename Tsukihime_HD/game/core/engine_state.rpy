## ==============================================================================
## core/engine_state.rpy - Persistent Progression & User Experience Settings
## ==============================================================================

## 1. Visual, Typography & Reading Preferences (Live-adjustable in Config)
default persistent.aspect_mode = "4x3_ambient"      # "4x3_ambient" | "4x3_black" | "16x9_full"
default persistent.story_font = "song"              # "song" (宋体) | "kai" (楷体) | "sans" (黑体)
default persistent.nvl_opacity = 0.72               # 0.35 .. 0.90 translucent dark glass veil
default persistent.nvl_font_size = 33               # 26 .. 40 px
default persistent.enable_ambient_lighting = True   # Dynamic sunset/night/deep-night character tint
default persistent.enable_cinematic_motion = True   # Subtle CG camera drift & impact pulses
default persistent.unlock_all_routes = False        # Preserved for existing players' unlock status
default persistent.ui_lang = None                   # None = auto-detect OS locale ("zh" | "en")

## 2. Authentic Cross-Playthrough Persistent Clear Flags (NScripter Global >= 200)
default persistent.execution_cnt = 0
default persistent.cleared = 0
default persistent.ark_normalcleared = 0

default persistent.clear_ark = 0
default persistent.clear_ciel = 0
default persistent.clear_akiha = 0
default persistent.clear_hisui = 0
default persistent.clear_kohaku = 0

default persistent.clear_ark_true = 0
default persistent.clear_ark_good = 0
default persistent.clear_ciel_true = 0
default persistent.clear_ciel_good = 0
default persistent.clear_akiha_true = 0
default persistent.clear_akiha_good = 0
default persistent.clear_hisui_true = 0
default persistent.clear_hisui_good = 0
default persistent.clear_kohaku_true = 0
default persistent.clear_kohaku_good = 0

## 3. Automatic CG Gallery Seen Registry
default persistent.seen_cgs = set()

init -3 python:
    import locale as _sys_locale

    def _detect_default_ui_lang():
        try:
            if sys.platform == "win32":
                import ctypes as _ct
                lid = _ct.windll.kernel32.GetUserDefaultUILanguage()
                if (lid & 0xFF) == 0x04:  # LANG_CHINESE
                    return "zh"
                return "en"
        except Exception:
            pass
        try:
            loc = (_sys_locale.getlocale()[0] or "").lower()
            if loc.startswith("zh") or "chinese" in loc:
                return "zh"
        except Exception:
            pass
        return "en"

    _DEFAULT_UI_LANG = _detect_default_ui_lang()

    def get_ui_lang():
        v = getattr(persistent, "ui_lang", None)
        return v if v in ("zh", "en") else _DEFAULT_UI_LANG

    def is_ui_en():
        return get_ui_lang() == "en"

    def ui_tr(zh, en):
        return en if is_ui_en() else zh

    BYOA_SPLASH_QUOTE = ""
    BYOA_SPLASH_SUB = ""
    # 100% Open-Source (SIL OFL 1.1) Story Typography; FontGroup ensures zero tofu on U+78A6 (碦)
    _KAI_FONT_GROUP = FontGroup().add("fonts/notoserif_sc.otf", 0x78A6, 0x78A6).add("fonts/lxgw_wenkai.ttf", 0x0000, 0x10FFFF)

    STORY_FONT_MAP = {
        "song": ("fonts/notoserif_sc.otf", "思源宋体 · 文学印刷"),
        "kai":  (_KAI_FONT_GROUP,          "霞鹜文楷 · 经典情怀"),
        "sans": ("fonts/notosans_med.otf", "思源黑体 · 现代护眼"),
    }

    ASPECT_MODE_MAP = {
        "4x3_ambient": "4:3 完整原画 · 柔焦氛围边",
        "4x3_black": "4:3 完整原画 · 纯黑影院边",
        "16x9_full": "16:9 沉浸满屏 · 智能顶偏",
    }

    CANONICAL_ENDINGS = [
        ("clear_ark_true", "s52a", "爱尔奎特 TRUE · 月姬"),
        ("clear_ark_good", "s53a", "爱尔奎特 GOOD · 白昼之月"),
        ("clear_ciel_true", "s310", "希耶尔 TRUE · 日光"),
        ("clear_ciel_good", "s308", "希耶尔 GOOD · 白昼之梦"),
        ("clear_akiha_true", "s385", "秋叶 TRUE · 苍之月"),
        ("clear_akiha_good", "s384", "秋叶 NORMAL · 四季之梦"),
        ("clear_hisui_true", "s412", "翡翠 TRUE · 拂晓之梦"),
        ("clear_hisui_good", "s413", "翡翠 GOOD · 阳向之梦"),
        ("clear_kohaku_true", "s429", "琥珀 TRUE · 阳向之梦"),
    ]

    def get_story_font():
        return STORY_FONT_MAP.get(persistent.story_font, STORY_FONT_MAP["song"])[0]

    def get_story_font_label():
        return STORY_FONT_MAP.get(persistent.story_font, STORY_FONT_MAP["song"])[1]

    def get_aspect_mode_label():
        return ASPECT_MODE_MAP.get(persistent.aspect_mode, ASPECT_MODE_MAP["4x3_ambient"])

    def is_ending_cleared(p_var, seen_lbl):
        return bool(getattr(persistent, p_var, 0) > 0 or renpy.seen_label(seen_lbl))

    def get_cleared_endings_count():
        return sum(1 for p_var, lbl, _ in CANONICAL_ENDINGS if is_ending_cleared(p_var, lbl))

    def can_enter_cleared_branch():
        """Day 1 unlocked choices after clearing any 1 route."""
        return bool(persistent.unlock_all_routes or persistent.cleared > 0 or get_cleared_endings_count() > 0)

    def can_enter_far_side():
        """Far Side (Akiha / Hisui / Kohaku) unlocks after clearing Arcueid or Ciel route."""
        return bool(
            persistent.unlock_all_routes
            or persistent.clear_ark > 0
            or persistent.clear_ciel > 0
            or is_ending_cleared("clear_ark_true", "s52a")
            or is_ending_cleared("clear_ciel_true", "s310")
        )

    def can_enter_hisui_unlocked():
        """Unlocks Kohaku Day-1 clue and Hisui Good End after clearing Hisui route."""
        return bool(
            persistent.unlock_all_routes
            or persistent.clear_hisui > 0
            or is_ending_cleared("clear_hisui_true", "s412")
        )

    def can_enter_kohaku():
        return can_enter_hisui_unlocked()

    def can_enter_ark_good():
        """Arcueid Good End unlocks after clearing Arcueid True End once."""
        return bool(
            persistent.unlock_all_routes
            or persistent.ark_normalcleared > 0
            or is_ending_cleared("clear_ark_true", "s52a")
        )

    def is_tsukishoku_unlocked():
        """Eclipse (月蝕) unlocks once all 9 canonical endings are cleared (or master unlock)."""
        if persistent.unlock_all_routes:
            return True
        if renpy.seen_label("eclipse"):
            return True
        return get_cleared_endings_count() >= len(CANONICAL_ENDINGS)

    def mark_cg_seen(cname):
        if not isinstance(persistent.seen_cgs, set):
            persistent.seen_cgs = set(persistent.seen_cgs) if persistent.seen_cgs else set()
        if cname not in persistent.seen_cgs:
            persistent.seen_cgs.add(cname)
            renpy.save_persistent()

    # ==========================================================================
    # BYOA Multi-Edition Compatibility Helpers (Dynamic Audio & Asset Gate)
    # ==========================================================================
    def tsuki_bgm_path(track_id):
        """Resolve BGM track 01..10 across WAV / FLAC / OGG / MP3 transparently."""
        tid = str(track_id).strip().replace("\\", "/").rsplit("/", 1)[-1].rsplit(".", 1)[0]
        if tid.isdigit():
            tid = f"{int(tid):02d}"
        for ext in ("wav", "flac", "ogg", "mp3"):
            cand = f"audio/{tid}.{ext}"
            if renpy.loadable(cand):
                return cand
        return None

    def tsuki_se_path(se_stem):
        """Resolve SE track across WAV / OGG / MP3 transparently."""
        stem = str(se_stem).strip().replace("\\", "/").rsplit("/", 1)[-1].rsplit(".", 1)[0]
        for ext in ("wav", "ogg", "mp3"):
            cand = f"audio/{stem}.{ext}"
            if renpy.loadable(cand):
                return cand
        return None

    def tsuki_play_bgm(track_id, fadein=1.2):
        """Play BGM safely; no-ops cleanly if optional BGM files were not imported."""
        p = tsuki_bgm_path(track_id)
        if p:
            renpy.music.play(p, channel="music", loop=True, fadein=fadein, if_changed=True)

    def tsuki_play_se(se_stem):
        """Play one-shot SE safely; no-ops cleanly if missing."""
        p = tsuki_se_path(se_stem)
        if p:
            renpy.music.play(p, channel="sound", loop=False, if_changed=False)

    def tsuki_play_ambient(se_stem, fadein=0.5):
        """Play looping ambient SFX safely; no-ops cleanly if missing."""
        p = tsuki_se_path(se_stem)
        if p:
            renpy.music.play(p, channel="ambient", loop=True, fadein=fadein, if_changed=True)

    def get_byoa_status():
        """Return live availability dict for user-imported BYOA asset categories."""
        return {
            "story":     renpy.has_label("f20") and renpy.has_label("s20"),
            "images":    renpy.loadable("images/bg/bg_01a.webp") and renpy.loadable("images/tachi/ark_t01a.webp"),
            "title_art": renpy.loadable("gui/main_menu.webp"),
            "portraits": renpy.loadable("gui/portraits/arc_norm.png"),
            "audio":     tsuki_bgm_path("08") is not None,
        }

    def is_byoa_assets_installed():
        st = get_byoa_status()
        return bool(st["story"] and st["images"] and st["title_art"])
