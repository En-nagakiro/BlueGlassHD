## ==============================================================================
## core/stage_engine.rpy - Dual-Aspect Cinema Stage, 3-Slot Tachi, True Monocro,
##                         NScripter Transitions & 3-Layer Chapter Title Cards
## ==============================================================================

## Rollback-safe stage state (never mutate dicts in-place!)
default _stage_kind = "solid"        # "solid" | "bg" | "cg" | "word"
default _stage_name = "#000000"
default _stage_monocro = None        # None or "#rrggbb"
default _stage_ambient = "day"       # "day" | "sunset" | "night" | "deep_night"
default _stage_slots = {"l": None, "c": None, "r": None}

init -2:
    ## Smooth cinematic camera drift transforms (16:9 mode when cinematic motion is enabled)
    transform tsuki_cg_drift_down:
        xysize (1920, 1440)
        xalign 0.5
        yalign 0.02
        easein 7.5 yalign 0.40

    transform tsuki_cg_slow_zoom:
        xysize (1920, 1440)
        xalign 0.5
        yalign 0.14
        zoom 1.0
        easein 6.5 zoom 1.06

    transform tsuki_bg_fit_16x9:
        xysize (1920, 1440)
        xalign 0.5
        yalign 0.5

    transform tsuki_cg_fit_16x9:
        xysize (1920, 1440)
        xalign 0.5
        yalign 0.08

    transform tsuki_fit_4x3:
        xysize (1440, 1080)
        xalign 0.5
        yalign 0.5

    ## Chapter day banner gentle fade-in (authentic NScripter 16-frame alpha ramp)
    transform tsuki_phase_day_fade(px, py):
        xpos px
        ypos py
        xysize (720, 90)
        alpha 0.0
        easein 0.55 alpha 1.0

    ## Flashes
    define flash_red = Fade(0.08, 0.0, 0.28, color="#ff0000")
    define flash_white = Fade(0.08, 0.0, 0.28, color="#ffffff")
    define flash_black = Fade(0.15, 0.0, 0.35, color="#000000")
    define flash_blue = Fade(0.08, 0.0, 0.25, color="#0044ff")

init -2 python:
    CINEMATIC_DRIFT_CGS = {
        "aki_e01", "aki_e01b", "ao_01", "ao_02", "ark_e01",
        "his_e08", "cmo_04a", "cmo_04b", "cmo_16", "cmo_20",
    }

    TSUKI_TRANSITIONS = {
        "nowaitdisp": None,
        "waitdisp": Dissolve(0.15),
        "crossfade_fst": Dissolve(0.28),
        "crossfade_mid": Dissolve(0.60),
        "crossfade_slw": Dissolve(1.25),
        "lshutter_fst": CropMove(0.28, "wipeleft"),
        "lshutter_mid": CropMove(0.55, "wipeleft"),
        "lshutter_slw": CropMove(1.05, "wipeleft"),
        "rshutter_fst": CropMove(0.28, "wiperight"),
        "rshutter_mid": CropMove(0.55, "wiperight"),
        "rshutter_slw": CropMove(1.05, "wiperight"),
        "tshutter_fst": CropMove(0.28, "wipeup"),
        "tshutter_mid": CropMove(0.55, "wipeup"),
        "tshutter_slw": CropMove(1.05, "wipeup"),
        "bshutter_fst": CropMove(0.28, "wipedown"),
        "bshutter_mid": CropMove(0.55, "wipedown"),
        "bshutter_slw": CropMove(1.05, "wipedown"),
        "lcartain_fst": CropMove(0.32, "wiperight"),
        "lcartain_mid": CropMove(0.62, "wiperight"),
        "lcartain_slw": CropMove(1.15, "wiperight"),
        "rcartain_fst": CropMove(0.32, "wipeleft"),
        "rcartain_mid": CropMove(0.62, "wipeleft"),
        "rcartain_slw": CropMove(1.15, "wipeleft"),
        "tcartain_fst": CropMove(0.32, "wipedown"),
        "tcartain_mid": CropMove(0.62, "wipedown"),
        "tcartain_slw": CropMove(1.15, "wipedown"),
        "bcartain_fst": CropMove(0.32, "wipeup"),
        "bcartain_mid": CropMove(0.62, "wipeup"),
        "bcartain_slw": CropMove(1.15, "wipeup"),
        "lscroll_fst": PushMove(0.35, "pushleft"),
        "lscroll_mid": PushMove(0.65, "pushleft"),
        "lscroll_slw": PushMove(1.10, "pushleft"),
        "rscroll_fst": PushMove(0.35, "pushright"),
        "rscroll_mid": PushMove(0.65, "pushright"),
        "rscroll_slw": PushMove(1.10, "pushright"),
        "tscroll_fst": PushMove(0.35, "pushup"),
        "tscroll_mid": PushMove(0.65, "pushup"),
        "tscroll_slw": PushMove(1.10, "pushup"),
        "bscroll_fst": PushMove(0.35, "pushdown"),
        "bscroll_mid": PushMove(0.65, "pushdown"),
        "bscroll_slw": PushMove(1.10, "pushdown"),
        "flash_red": Fade(0.08, 0.0, 0.28, color="#ff0000"),
        "flash_white": Fade(0.08, 0.0, 0.28, color="#ffffff"),
        "flash_black": Fade(0.15, 0.0, 0.35, color="#000000"),
        "flash_blue": Fade(0.08, 0.0, 0.25, color="#0044ff"),
    }

    def tsuki_get_transition(name):
        if name is None:
            return None
        if not isinstance(name, str):
            return name
        return TSUKI_TRANSITIONS.get(name, Dissolve(0.45))

    def _compute_monocro_matrix(hex_col):
        if not hex_col:
            return IdentityMatrix()
        # Authentic grayscale + tint on scene/tachi layers (never washes out NVL text!)
        return TintMatrix(hex_col) * SaturationMatrix(0.0)

    def _compute_ambient_matrix(ambient_key):
        if not persistent.enable_ambient_lighting:
            return IdentityMatrix()
        if ambient_key == "sunset":
            return TintMatrix("#fff2e8") * ContrastMatrix(1.02)
        elif ambient_key == "night":
            return TintMatrix("#eaf0ff") * BrightnessMatrix(-0.025) * ContrastMatrix(1.02)
        elif ambient_key == "deep_night":
            return TintMatrix("#dfe8ff") * BrightnessMatrix(-0.045) * ContrastMatrix(1.04)
        return IdentityMatrix()

    def _infer_ambient(bname):
        if bname.startswith("ima_"):
            return store._stage_ambient
        if bname.endswith("b"):
            return "sunset"
        elif bname.endswith("c"):
            return "night"
        elif bname.endswith(("d", "e", "f", "g")):
            return "deep_night"
        elif bname.endswith("a"):
            return "day"
        return "day"

    def _resolve_stage_displayable(kind, name):
        if kind == "bg":
            path = BG_FILES.get(name)
            return Image(path) if path else Solid("#000000")
        elif kind == "cg":
            path = CG_FILES.get(name)
            return Image(path) if path else Solid("#000000")
        elif kind == "word":
            path = WORD_FILES.get(name)
            return Image(path) if path else Solid("#000000")
        else:
            col = name if (isinstance(name, str) and name.startswith("#")) else "#000000"
            return Solid(col)

    def _render_pillars(kind, name, monocro):
        """Render outer 240px left/right cinema bands at zorder 25 (cleanly clips 4:3 stage & wide tachi)."""
        mode = persistent.aspect_mode
        if mode == "16x9_full":
            renpy.hide("pillar_left")
            renpy.hide("pillar_right")
            return

        if mode == "4x3_black" or kind == "solid" or (kind == "bg" and name in ("ima_10", "ima_11")):
            left_band = Solid("#000000", xsize=240, ysize=1080)
            right_band = Solid("#000000", xsize=240, ysize=1080)
        else:
            base = _resolve_stage_displayable(kind, name)
            mat = _compute_monocro_matrix(monocro) * BrightnessMatrix(-0.44) * SaturationMatrix(0.62)
            blurred_full = Transform(
                base,
                xysize=(1920, 1440),
                blur=44.0,
                matrixcolor=mat,
            )
            # Crop left 240px and right 240px from the centered 1920x1080 band (y=180..1260)
            left_band = Composite(
                (240, 1080),
                (0, 0), Crop((0, 180, 240, 1080), blurred_full),
                (239, 0), Solid("#3b648f55", xsize=1, ysize=1080),
            )
            right_band = Composite(
                (240, 1080),
                (0, 0), Crop((1680, 180, 240, 1080), blurred_full),
                (0, 0), Solid("#3b648f55", xsize=1, ysize=1080),
            )

        renpy.show("pillar_left", what=left_band, at_list=[Transform(xpos=0, ypos=0)], zorder=25)
        renpy.show("pillar_right", what=right_band, at_list=[Transform(xpos=1680, ypos=0)], zorder=25)

    def _render_stage_bg(kind, name, monocro):
        base = _resolve_stage_displayable(kind, name)
        mat = _compute_monocro_matrix(monocro)
        mode = persistent.aspect_mode

        if kind == "solid":
            disp = Transform(base, xysize=(1920, 1080), xalign=0.5, yalign=0.5)
            renpy.show("stage_bg", what=disp, zorder=10)
            return

        if mode == "16x9_full" and kind != "word":
            if kind == "cg":
                if persistent.enable_cinematic_motion and name in CINEMATIC_DRIFT_CGS:
                    disp = Transform(base, matrixcolor=mat)
                    renpy.show("stage_bg", what=disp, at_list=[tsuki_cg_drift_down], zorder=10)
                else:
                    disp = Transform(base, matrixcolor=mat)
                    renpy.show("stage_bg", what=disp, at_list=[tsuki_cg_fit_16x9], zorder=10)
            else:
                if persistent.enable_cinematic_motion and name in CINEMATIC_DRIFT_CGS:
                    disp = Transform(base, matrixcolor=mat)
                    renpy.show("stage_bg", what=disp, at_list=[tsuki_cg_drift_down], zorder=10)
                else:
                    disp = Transform(base, matrixcolor=mat)
                    renpy.show("stage_bg", what=disp, at_list=[tsuki_bg_fit_16x9], zorder=10)
        else:
            # 4:3 zero-crop presentation (1440x1080 centered, exact aspect fidelity!)
            disp = Transform(base, xysize=(1440, 1080), xalign=0.5, yalign=0.5, matrixcolor=mat)
            renpy.show("stage_bg", what=disp, zorder=10)

    _TACHI_ZOOM_CACHE = {}

    def _get_tachi_zoom(path):
        """Compute exact vertical zoom so 1x (480px), 2x (960px), and 4x (1920px) sprites all fill 1080p identically."""
        z = _TACHI_ZOOM_CACHE.get(path)
        if z is not None:
            return z
        try:
            _, h = renpy.image_size(path)
            z = 1080.0 / float(h) if h and h > 0 else 0.5625
        except Exception:
            z = 0.5625
        _TACHI_ZOOM_CACHE[path] = z
        return z

    def _render_tachi_slot(slot, tname):
        tag = f"tachi_{slot}"
        if not tname:
            renpy.hide(tag)
            return
        path = TACHI_FILES.get(tname)
        if not path:
            return

        if persistent.aspect_mode == "16x9_full":
            xpos_map = {"l": 480, "c": 960, "r": 1440}
        else:
            # Centered symmetrically inside the 1440px 4:3 frame (x=240..1680)
            xpos_map = {"l": 600, "c": 960, "r": 1320}

        mat = _compute_monocro_matrix(store._stage_monocro) * _compute_ambient_matrix(store._stage_ambient)
        t_zoom = _get_tachi_zoom(path)
        disp = Transform(
            Image(path),
            zoom=t_zoom,
            xpos=xpos_map[slot],
            xanchor=0.5,
            yalign=1.0,
            matrixcolor=mat,
        )
        renpy.show(tag, what=disp, zorder=20)

    def tsuki_clear_stage():
        store._stage_kind = "solid"
        store._stage_name = "#000000"
        store._stage_monocro = None
        store._stage_ambient = "day"
        store._stage_slots = {"l": None, "c": None, "r": None}
        for tag in ("tachi_l", "tachi_c", "tachi_r", "phase_a", "phase_b", "pillar_left", "pillar_right"):
            renpy.hide(tag)
        renpy.show("stage_bg", what=Solid("#000000", xsize=1920, ysize=1080), zorder=10)

    def _apply_trans(trans):
        t = tsuki_get_transition(trans)
        if t is not None:
            renpy.with_statement(t)

    def tsuki_bg(name, trans="crossfade_mid"):
        # NScripter `bg` clears all active standing sprites
        for slot in ("l", "c", "r"):
            renpy.hide(f"tachi_{slot}")
        renpy.hide("phase_a")
        renpy.hide("phase_b")
        store._stage_slots = {"l": None, "c": None, "r": None}
        store._stage_kind = "bg"
        store._stage_name = name
        store._stage_ambient = _infer_ambient(name)

        if name.startswith("cmo_"):
            mark_cg_seen(name)

        _render_stage_bg("bg", name, store._stage_monocro)
        _render_pillars("bg", name, store._stage_monocro)
        _apply_trans(trans)

    def tsuki_cg(name, trans="crossfade_mid"):
        for slot in ("l", "c", "r"):
            renpy.hide(f"tachi_{slot}")
        renpy.hide("phase_a")
        renpy.hide("phase_b")
        store._stage_slots = {"l": None, "c": None, "r": None}
        store._stage_kind = "cg"
        store._stage_name = name
        mark_cg_seen(name)

        _render_stage_bg("cg", name, store._stage_monocro)
        _render_pillars("cg", name, store._stage_monocro)
        _apply_trans(trans)

    def tsuki_word_bg(name, trans="crossfade_mid"):
        for slot in ("l", "c", "r"):
            renpy.hide(f"tachi_{slot}")
        renpy.hide("phase_a")
        renpy.hide("phase_b")
        store._stage_slots = {"l": None, "c": None, "r": None}
        store._stage_kind = "word"
        store._stage_name = name

        _render_stage_bg("word", name, store._stage_monocro)
        _render_pillars("word", name, store._stage_monocro)
        _apply_trans(trans)

    def tsuki_solid(color_hex, trans="crossfade_mid"):
        for slot in ("l", "c", "r"):
            renpy.hide(f"tachi_{slot}")
        renpy.hide("phase_a")
        renpy.hide("phase_b")
        store._stage_slots = {"l": None, "c": None, "r": None}
        store._stage_kind = "solid"
        store._stage_name = color_hex

        _render_stage_bg("solid", color_hex, store._stage_monocro)
        _render_pillars("solid", color_hex, store._stage_monocro)
        _apply_trans(trans)

    def tsuki_ld(slot, tname, trans="crossfade_fst"):
        if slot not in ("l", "c", "r"):
            return
        new_slots = dict(store._stage_slots)
        new_slots[slot] = tname
        store._stage_slots = new_slots
        _render_tachi_slot(slot, tname)
        _apply_trans(trans)

    def tsuki_cl(slot, trans="crossfade_fst"):
        new_slots = dict(store._stage_slots)
        if slot == "a":
            for s in ("l", "c", "r"):
                new_slots[s] = None
                renpy.hide(f"tachi_{s}")
        elif slot in ("l", "c", "r"):
            new_slots[slot] = None
            renpy.hide(f"tachi_{slot}")
        store._stage_slots = new_slots
        _apply_trans(trans)

    def tsuki_monocro(color_hex, trans="crossfade_fst"):
        store._stage_monocro = color_hex
        _render_stage_bg(store._stage_kind, store._stage_name, color_hex)
        _render_pillars(store._stage_kind, store._stage_name, color_hex)
        for s, tname in store._stage_slots.items():
            if tname:
                _render_tachi_slot(s, tname)
        _apply_trans(trans)

    def tsuki_flash(color_hex="#ffffff"):
        renpy.with_statement(Fade(0.06, 0.0, 0.22, color=color_hex))

    def tsuki_cinematic_pulse(kind="red"):
        if not persistent.enable_cinematic_motion:
            return
        if kind == "red":
            renpy.with_statement(flash_red)
            renpy.with_statement(vpunch)
        elif kind == "white":
            renpy.with_statement(flash_white)

    def tsuki_refresh_stage():
        """Re-render active stage immediately after changing aspect_mode / lighting in Preferences."""
        if renpy.context()._main_menu:
            return
        _render_stage_bg(store._stage_kind, store._stage_name, store._stage_monocro)
        _render_pillars(store._stage_kind, store._stage_name, store._stage_monocro)
        for s, tname in store._stage_slots.items():
            if tname:
                _render_tachi_slot(s, tname)

    config.after_load_callbacks.append(tsuki_refresh_stage)


## ==============================================================================
## Authentic 3-Layer Tsukihime Chapter Title Card Sequences
## ($phasebg + $phasetitle_a half-screen calligraphy + $phasetitle_b day badge)
## ==============================================================================
label tsuki_left_phase:
    nvl clear
    python:
        # 1. Background image wipes in from left
        if phase_bg:
            if phase_bg_kind == "cg" and phase_bg in CG_FILES:
                tsuki_cg(phase_bg, "lcartain_fst")
            elif phase_bg in BG_FILES:
                tsuki_bg(phase_bg, "lcartain_fst")
            else:
                tsuki_solid("#000000", "crossfade_fst")
        else:
            tsuki_solid("#000000", "crossfade_fst")

        # 2. Half-screen vertical calligraphic title card on LEFT half of 4:3 frame
        if phase_title_a and phase_title_a in WORD_FILES:
            p_a = WORD_FILES[phase_title_a]
            px_a = 240 if persistent.aspect_mode != "16x9_full" else 0
            w_a = 720 if persistent.aspect_mode != "16x9_full" else 960
            disp_a = Transform(Image(p_a), xysize=(w_a, 1080), xpos=px_a, ypos=0)
            renpy.show("phase_a", what=disp_a, zorder=22)
            renpy.with_statement(tsuki_get_transition("rcartain_fst"))

        # 3. Day badge fades in at top-left (NScripter 0, 48 -> 240, 108 in 1080p 4:3)
        if phase_title_b and phase_title_b in WORD_FILES:
            p_b = WORD_FILES[phase_title_b]
            px_b = 240 if persistent.aspect_mode != "16x9_full" else 80
            renpy.show("phase_b", what=Image(p_b), at_list=[tsuki_phase_day_fade(px_b, 108)], zorder=23)

    $ renpy.pause(2.2)
    $ renpy.hide("phase_a")
    $ renpy.hide("phase_b")
    $ tsuki_solid("#000000", "crossfade_fst")
    $ renpy.pause(0.35)
    return


label tsuki_right_phase:
    nvl clear
    python:
        # 1. Background image wipes in from right
        if phase_bg:
            if phase_bg_kind == "cg" and phase_bg in CG_FILES:
                tsuki_cg(phase_bg, "rcartain_fst")
            elif phase_bg in BG_FILES:
                tsuki_bg(phase_bg, "rcartain_fst")
            else:
                tsuki_solid("#000000", "crossfade_fst")
        else:
            tsuki_solid("#000000", "crossfade_fst")

        # 2. Half-screen vertical calligraphic title card on RIGHT half of 4:3 frame
        if phase_title_a and phase_title_a in WORD_FILES:
            p_a = WORD_FILES[phase_title_a]
            px_a = 960
            w_a = 720 if persistent.aspect_mode != "16x9_full" else 960
            disp_a = Transform(Image(p_a), xysize=(w_a, 1080), xpos=px_a, ypos=0)
            renpy.show("phase_a", what=disp_a, zorder=22)
            renpy.with_statement(tsuki_get_transition("lcartain_fst"))

        # 3. Day badge fades in at bottom-right (NScripter 320, 440 -> 960, 960 in 1080p 4:3)
        if phase_title_b and phase_title_b in WORD_FILES:
            p_b = WORD_FILES[phase_title_b]
            px_b = 960
            renpy.show("phase_b", what=Image(p_b), at_list=[tsuki_phase_day_fade(px_b, 955)], zorder=23)

    $ renpy.pause(2.2)
    $ renpy.hide("phase_a")
    $ renpy.hide("phase_b")
    $ tsuki_solid("#000000", "crossfade_fst")
    $ renpy.pause(0.35)
    return


label tsuki_center_phase:
    call tsuki_right_phase
    return
