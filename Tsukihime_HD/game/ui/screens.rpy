## ==============================================================================
## ui/screens.rpy - Plan A "Frosted Mist" (薄雾琉璃) Soft Minimalist Cinema UI
## Slender DengXian Typography + 2x Supersampled Rounded Glass + Pill Switches
## ==============================================================================

init offset = -1

init -1 python:
    def get_bgm_vol_pct():
        try:
            return int(round(_preferences.get_mixer("music") * 100))
        except Exception:
            return 100

    def get_sfx_vol_pct():
        try:
            return int(round(_preferences.get_mixer("sfx") * 100))
        except Exception:
            return 100

    # Soft Morandi-pastel Heroine Portrait & Affection definitions (Plan 3: Near 2 + Far 3)
    NEAR_HEROINE_PROFILES = [
        ("arc",  "爱尔奎特", "ARCUEID", "ark_regard", "#dec894", [
            ("clear_ark_true", "s52a", "TRUE · 月姬",     "TRUE · Moon Princess"),
            ("clear_ark_good", "s53a", "GOOD · 白昼之月", "GOOD · Dawn Moon"),
        ]),
        ("ciel", "希耶尔",   "CIEL",    "ciel_regard", "#98c2e2", [
            ("clear_ciel_true", "s310", "TRUE · 日光",     "TRUE · Sunlight"),
            ("clear_ciel_good", "s308", "GOOD · 白昼之梦", "GOOD · Daydream"),
        ]),
    ]

    FAR_HEROINE_PROFILES = [
        ("akiha",  "远野秋叶", "AKIHA",  "akiha_regard",  "#d698a3", [
            ("clear_akiha_true", "s385", "TRUE · 苍之月",     "TRUE · Blue Moon"),
            ("clear_akiha_good", "s384", "NORMAL · 四季之梦", "NORMAL · Distant Dream"),
        ]),
        ("hisui",  "翡翠",     "HISUI",  "hisui_regard",  "#9ac9cf", [
            ("clear_hisui_true", "s412", "TRUE · 拂晓之梦", "TRUE · Dream at Dawn"),
            ("clear_hisui_good", "s413", "GOOD · 阳向之梦", "GOOD · Sunny Dream"),
        ]),
        ("kohaku", "琥珀",     "KOHAKU", "kohaku_regard", "#ddb692", [
            ("clear_kohaku_true", "s429", "TRUE · 阳向之梦", "TRUE · Sunny Garden"),
        ]),
    ]

    def get_heroine_affection(var_name):
        try:
            return max(0, int(getattr(store, var_name, 0)))
        except Exception:
            return 0


## ==============================================================================
## Soft Fluid Micro-Motion
## ==============================================================================
transform menu_item_reveal(delay_sec=0.0):
    alpha 0.0 xoffset -8
    pause delay_sec
    easein 0.28 alpha 1.0 xoffset 0

transform choice_fade_in(idx=0):
    alpha 0.0 yoffset 8
    pause (idx * 0.05)
    easein 0.26 alpha 1.0 yoffset 0

transform modal_backdrop_fade:
    alpha 0.0
    easein 0.18 alpha 1.0

transform modal_editorial_in:
    alpha 0.0 yoffset 10
    easein 0.22 alpha 1.0 yoffset 0

# Eclipse (月蝕) Animated Title Screen GL2 Parallax Cloud, Corona & Crystal Shard Transforms
transform title_cloud_loop_ltr(period=60.0, y_pos=520, alpha_val=1.0):
    subpixel True
    ypos y_pos
    alpha alpha_val
    xpos -1920
    linear period xpos 0
    repeat

transform title_corona_breathe:
    subpixel True
    blend "add"
    xpos 850
    ypos 16
    alpha 0.36
    easein_quad 3.4 alpha 0.72
    easeout_quad 3.4 alpha 0.36
    repeat

transform title_motes_float(period=11.0, start_y=160, rise=72, x_pos=810, sway=12):
    subpixel True
    xpos x_pos
    ypos start_y
    xoffset 0
    alpha 0.0
    parallel:
        linear period ypos (start_y - rise)
    parallel:
        easein (period * 0.25) alpha 0.92
        pause (period * 0.45)
        easeout (period * 0.30) alpha 0.0
    parallel:
        ease (period * 0.5) xoffset sway
        ease (period * 0.5) xoffset 0
    repeat


## ==============================================================================
## Base Styles - Slender DengXian UI & Smooth Rounded Circular-Thumb Sliders
## ==============================================================================
style default:
    properties gui.text_properties()
    language gui.language

style input:
    properties gui.text_properties("input", accent=True)
    adjust_spacing False

style hyperlink_text:
    properties gui.text_properties("hyperlink", accent=True)
    hover_underline True

style gui_text:
    properties gui.text_properties("interface")

style button:
    properties gui.button_properties("button")
    hover_sound "audio/ui_hover.wav"
    activate_sound "audio/ui_click.wav"

style button_text is gui_text:
    properties gui.text_properties("button")
    yalign 0.5

style label_text is gui_text:
    properties gui.text_properties("label", accent=True)

style prompt_text is gui_text:
    properties gui.text_properties("prompt")

style bar:
    ysize 22
    left_bar Frame("gui/slider/hairline_fill.png", 6, 0)
    right_bar Frame("gui/slider/hairline_track.png", 6, 0)
    thumb "gui/slider/hairline_thumb.png"
    hover_thumb "gui/slider/hairline_thumb_hover.png"
    left_gutter 11
    right_gutter 11
    thumb_offset 11

style vbar:
    xsize 6
    top_bar Solid("#dce8f524")
    bottom_bar Solid("#a2c6e6")

style scrollbar:
    ysize 6
    base_bar Solid("#dce8f514")
    thumb Solid("#8fa6be66")
    hover_thumb Solid("#a2c6e6cc")

style vscrollbar:
    xsize 6
    base_bar Solid("#dce8f514")
    thumb Solid("#8fa6be66")
    hover_thumb Solid("#a2c6e6cc")

style slider:
    ysize 22
    left_bar Frame("gui/slider/hairline_fill.png", 6, 0)
    right_bar Frame("gui/slider/hairline_track.png", 6, 0)
    thumb "gui/slider/hairline_thumb.png"
    hover_thumb "gui/slider/hairline_thumb_hover.png"
    left_gutter 11
    right_gutter 11
    thumb_offset 11

style vslider:
    xsize 22
    base_bar Solid("#dce8f528")
    thumb "gui/slider/hairline_thumb.png"
    thumb_offset 11

style frame:
    padding (0, 0)
    background None


## ==============================================================================
## Full-Screen Type-Moon NVL Screen (Pure Literary Canvas)
## ==============================================================================
screen nvl(dialogue, items=None):
    $ is_4x3 = (persistent.aspect_mode != "16x9_full")
    $ veil_w = 1440 if is_4x3 else 1920
    $ col_w = 1180 if is_4x3 else 1280
    $ cur_font = get_story_font()
    $ cur_size = int(persistent.nvl_font_size)
    $ has_content = bool(dialogue or items)

    if has_content:
        window:
            style "nvl_window"
            xsize veil_w
            ysize 1080
            xalign 0.5
            ypos 0
            background Transform(Solid("#060a12"), alpha=persistent.nvl_opacity)
            padding (0, 0)

            vbox:
                xalign 0.5
                ypos 74
                xsize col_w
                spacing 14

                for d in dialogue:
                    window:
                        style "nvl_entry"
                        id d.window_id
                        background None
                        padding (0, 0)
                        xfill True
                        ysize None

                        text d.what:
                            id d.what_id
                            font cur_font
                            size cur_size
                            color "#eef4fa"
                            line_spacing 15
                            outlines [(1, "#000000cc", 0, 1)]
                            adjust_spacing False

                if items:
                    null height 20
                    for i in items:
                        textbutton i.caption:
                            action i.action
                            style "nvl_button"


style nvl_window is empty
style nvl_entry is empty
style nvl_label is default
style nvl_dialogue is default
style nvl_button is button
style nvl_button_text is button_text


## ==============================================================================
## Fallback ADV Say Screen & Input Screen
## ==============================================================================
screen say(who, what):
    window:
        id "window"
        if who is not None:
            window:
                style "namebox"
                text who id "who"
        text what id "what" font get_story_font() size int(persistent.nvl_font_size)

style window is default
style say_label is default
style say_dialogue is default
style say_thought is say_dialogue
style namebox is default
style namebox_label is say_label

style window:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height
    background Solid("#090d16e6")

style namebox:
    xpos gui.name_xpos
    xanchor gui.name_xalign
    xsize gui.namebox_width
    ypos gui.name_ypos
    ysize gui.namebox_height
    background Frame("gui/mist/pill_idle.png", 20, 14)
    padding (18, 6)

style say_label:
    properties gui.text_properties("name", accent=True)
    xalign gui.name_xalign
    yalign 0.5

style say_dialogue:
    properties gui.text_properties("dialogue")
    xpos gui.dialogue_xpos
    xsize gui.dialogue_width
    ypos gui.dialogue_ypos
    outlines [(1, "#000000cc", 0, 1)]
    line_spacing 8
    adjust_spacing False

screen input(prompt):
    style_prefix "input"
    window:
        vbox:
            xanchor gui.dialogue_text_xalign
            xpos gui.dialogue_xpos
            xsize gui.dialogue_width
            ypos gui.dialogue_ypos
            text prompt style "input_prompt"
            input id "input"

style input_prompt is default
style input_prompt:
    xalign gui.dialogue_text_xalign
    properties gui.text_properties("input_prompt")
style input:
    xalign gui.dialogue_text_xalign
    xmaximum gui.dialogue_width


## ==============================================================================
## Choice Screen - Silky Frosted Rounded Glass Capsules
## ==============================================================================
screen choice(items):
    style_prefix "choice"

    add Solid("#070b147a")

    vbox:
        xalign 0.5
        yalign 0.46
        spacing 16

        for idx, i in enumerate(items):
            $ was_chosen = bool(i.chosen)

            button:
                action i.action
                hover_sound "audio/ui_hover.wav"
                activate_sound "audio/ui_choice.wav"
                xsize 1040
                ysize 68
                background Frame("gui/mist/choice_idle.png", 22, 20)
                hover_background Frame("gui/mist/choice_hover.png", 22, 20)
                padding (0, 0)
                at choice_fade_in(idx)

                fixed:
                    xfill True
                    yfill True

                    if was_chosen:
                        hbox:
                            xpos 26
                            yalign 0.5
                            spacing 6
                            add Transform("gui/icons/check.png", zoom=0.46) yalign 0.5
                            text ui_tr("已选", "Seen") size 13 color "#92cfb9" font "fonts/lxgw_xihei.ttf" yalign 0.5

                    text i.caption:
                        xalign 0.5
                        yalign 0.5
                        size 25
                        color ("#9fb3c8" if was_chosen else "#eef4fa")
                        hover_color "#ffffff"
                        font get_story_font()
                        outlines [(1, "#00000088", 0, 1)]


## ==============================================================================
## Floating Soft Frosted Quick Menu (Zero 4:3 overlap!)
## ==============================================================================
default quick_menu = True

screen quick_menu():
    zorder 100

    if quick_menu and not main_menu:
        frame:
            xalign 0.986
            yalign 0.988
            background Frame("gui/mist/quick_pill.png", 20, 16)
            padding (18, 7)

            hbox:
                spacing 16

                $ qbuttons = [
                    ("Q.SAVE", QuickSave()),
                    ("Q.LOAD", QuickLoad()),
                    ("SAVE", ShowMenu("save")),
                    ("LOAD", ShowMenu("load")),
                    ("AUTO", Preference("auto-forward", "toggle")),
                    ("SKIP", Skip()),
                    ("TREE", ShowMenu("flowchart")),
                    ("LOG", ShowMenu("history")),
                    ("CONFIG", ShowMenu("preferences")),
                ]

                for label_text, act in qbuttons:
                    button:
                        action act
                        background None
                        hover_background None
                        padding (2, 1)
                        text label_text size 12 color "#92a5ba" hover_color "#ffffff" selected_color "#a2c6e6" font "fonts/lxgw_xihei.ttf"


init python:
    config.overlay_screens.append("quick_menu")


## ==============================================================================
## Main Menu - Option B Asymmetric Title Screen with Soft Frosted Hover Pills
## ==============================================================================
screen main_menu():
    tag menu

    if not is_byoa_assets_installed():
        use byoa_setup_required
    else:
        $ newest = renpy.newest_slot()
        $ tsuki_unlocked = is_tsukishoku_unlocked()
        $ cleared_cnt = get_cleared_endings_count()
        $ _mm_bgm = tsuki_bgm_path("08")

        if tsuki_unlocked and renpy.loadable("gui/title_eclipse_moon.png") and renpy.loadable("gui/title_eclipse_kanji.png"):
            # Post-5-Route Clear (Eclipse / 月蝕): Rich Saturated Cobalt-Violet Sky + Live Seamless Parallax Clouds
            add "gui/main_menu_eclipse_sky.webp"

            # Layer 1: Upper-sky moonlit cotton wisps drifting gently BEHIND the moon
            hbox at title_cloud_loop_ltr(period=94.0, y_pos=0, alpha_val=0.86):
                spacing 0
                add "gui/title_cloud_high.png"
                add "gui/title_cloud_high.png"

            # Layer 2: Radiant Full Moon + Breathing Additive Ice-Cyan / Amethyst Corona
            add "gui/title_eclipse_moon.png" xpos 850 ypos 16
            add "gui/title_eclipse_corona.png" at title_corona_breathe

            # Layer 3: Billowing moonlit violet-lavender cumulus sea (mid-far parallax)
            hbox at title_cloud_loop_ltr(period=56.0, y_pos=520, alpha_val=0.96):
                spacing 0
                add "gui/title_cloud_far.png"
                add "gui/title_cloud_far.png"

            # Layer 4: Authentic white-filled, deep-indigo-outlined `月姫` calligraphy + drifting blue glass shards
            add "gui/title_eclipse_kanji.png" xpos 1150 ypos 160
            add "gui/title_motes_a.png" at title_motes_float(period=11.0, start_y=165, rise=66, x_pos=810, sway=12)
            add "gui/title_motes_b.png" at title_motes_float(period=15.0, start_y=190, rise=82, x_pos=825, sway=-14)

            # Layer 5: Foreground silky translucent amethyst mist gliding smoothly across lower moon rim
            hbox at title_cloud_loop_ltr(period=34.0, y_pos=650, alpha_val=0.84):
                spacing 0
                add "gui/title_cloud_near.png"
                add "gui/title_cloud_near.png"

            # Layer 6: Velvet-indigo left spine readability gradient (keeps left menu text crystal-clear)
            add "gui/title_eclipse_left_veil.png" xpos 0 ypos 0
        else:
            add "gui/main_menu.webp"

        on "show" action If(_mm_bgm and not renpy.music.is_playing("music"), Play("music", _mm_bgm, fadein=1.5))
        on "replace" action If(_mm_bgm and not renpy.music.is_playing("music"), Play("music", _mm_bgm, fadein=1.5))

        # Editorial Epigraph & Edition Header (Top-Left Spine X=136)
        vbox:
            xpos 136
            ypos 148
            spacing 14

            text "CLASSIC HD  ·  BYOA EDITION" size 12 color ("#bab4ec" if tsuki_unlocked else "#8398b0") font "fonts/lxgw_xihei.ttf" kerning 2

            vbox:
                spacing 4
                text "Blue Blue Glass Moon," size 30 color ("#f5f4ff" if tsuki_unlocked else "#eaf1f9") font "fonts/lora_italic.ttf"
                text "Under The Crimson Air." size 30 color ("#d0c4f8" if tsuki_unlocked else "#a4bdd6") font "fonts/lora_italic.ttf"

            fixed:
                xsize 280
                ysize 2
                add Solid(("#d8ccff38" if tsuki_unlocked else "#dce8f528"), xsize=280, ysize=1) yalign 0.5
                add Solid(("#c6a8ff" if tsuki_unlocked else "#a2c6e6"), xsize=44, ysize=2) yalign 0.5

        # Soft Rounded Frosted-Mist Hover Menu Column (Flush X=136 spine!)
        vbox:
            xpos 116
            ypos 360
            spacing 4

            $ cont_hov = Frame("gui/mist/nav_hover.png", 18, 16) if newest else None
            $ std_hov = Frame("gui/mist/nav_hover.png", 18, 16)
            $ quit_hov = Frame("gui/mist/nav_rose_hover.png", 18, 16)
            $ ecl_hov = Frame("gui/mist/nav_gold_hover.png", 18, 16)

            # 1. CONTINUE
            button:
                xsize 344
                ysize 46
                action (FileLoad(newest, confirm=False) if newest else None)
                background None
                hover_background cont_hov
                padding (0, 0)
                at menu_item_reveal(0.00)
                fixed:
                    xfill True
                    yfill True
                    text "CONTINUE" xpos 20 yalign 0.5 size 20 font "fonts/lora_reg.ttf" kerning 3 color ("#dce6f2" if newest else "#485669") hover_color ("#ffffff" if newest else "#485669") insensitive_color "#485669"
                    if not is_ui_en():
                        text "继续" xpos 248 yalign 0.52 size 15 font "fonts/lxgw_xihei.ttf" color ("#8fa3ba" if newest else "#3a4656") hover_color ("#dce8f5" if newest else "#3a4656") insensitive_color "#3a4656"

            # 2. NEW GAME
            button:
                xsize 344
                ysize 46
                action Start()
                background None
                hover_background std_hov
                padding (0, 0)
                at menu_item_reveal(0.04)
                fixed:
                    xfill True
                    yfill True
                    text "NEW GAME" xpos 20 yalign 0.5 size 20 font "fonts/lora_reg.ttf" kerning 3 color "#e8f0f9" hover_color "#ffffff"
                    if not is_ui_en():
                        text "初章" xpos 248 yalign 0.52 size 15 font "fonts/lxgw_xihei.ttf" color "#92a7be" hover_color "#eef4fa"

            # 3. LOAD GAME
            button:
                xsize 344
                ysize 46
                action ShowMenu("load")
                background None
                hover_background std_hov
                padding (0, 0)
                at menu_item_reveal(0.08)
                fixed:
                    xfill True
                    yfill True
                    text "LOAD GAME" xpos 20 yalign 0.5 size 20 font "fonts/lora_reg.ttf" kerning 3 color "#dce6f2" hover_color "#ffffff"
                    if not is_ui_en():
                        text "读档" xpos 248 yalign 0.52 size 15 font "fonts/lxgw_xihei.ttf" color "#8fa3ba" hover_color "#dce8f5"

            # 4. FLOWCHART
            button:
                xsize 344
                ysize 46
                action ShowMenu("flowchart")
                background None
                hover_background std_hov
                padding (0, 0)
                at menu_item_reveal(0.12)
                fixed:
                    xfill True
                    yfill True
                    text "FLOWCHART" xpos 20 yalign 0.5 size 20 font "fonts/lora_reg.ttf" kerning 3 color "#dce6f2" hover_color "#ffffff"
                    if not is_ui_en():
                        text "分支" xpos 248 yalign 0.52 size 15 font "fonts/lxgw_xihei.ttf" color "#8fa3ba" hover_color "#dce8f5"

            # 5. GALLERY
            button:
                xsize 344
                ysize 46
                action ShowMenu("cg_gallery")
                background None
                hover_background std_hov
                padding (0, 0)
                at menu_item_reveal(0.16)
                fixed:
                    xfill True
                    yfill True
                    text "GALLERY" xpos 20 yalign 0.5 size 20 font "fonts/lora_reg.ttf" kerning 3 color "#dce6f2" hover_color "#ffffff"
                    if not is_ui_en():
                        text "画廊" xpos 248 yalign 0.52 size 15 font "fonts/lxgw_xihei.ttf" color "#8fa3ba" hover_color "#dce8f5"

            # 6. SOUND TEST
            button:
                xsize 344
                ysize 46
                action ShowMenu("music_room")
                background None
                hover_background std_hov
                padding (0, 0)
                at menu_item_reveal(0.20)
                fixed:
                    xfill True
                    yfill True
                    text "SOUND TEST" xpos 20 yalign 0.5 size 20 font "fonts/lora_reg.ttf" kerning 3 color "#dce6f2" hover_color "#ffffff"
                    if not is_ui_en():
                        text "音乐" xpos 248 yalign 0.52 size 15 font "fonts/lxgw_xihei.ttf" color "#8fa3ba" hover_color "#dce8f5"

            # 7. CONFIG
            button:
                xsize 344
                ysize 46
                action ShowMenu("preferences")
                background None
                hover_background std_hov
                padding (0, 0)
                at menu_item_reveal(0.24)
                fixed:
                    xfill True
                    yfill True
                    text "CONFIG" xpos 20 yalign 0.5 size 20 font "fonts/lora_reg.ttf" kerning 3 color "#dce6f2" hover_color "#ffffff"
                    if not is_ui_en():
                        text "设置" xpos 248 yalign 0.52 size 15 font "fonts/lxgw_xihei.ttf" color "#8fa3ba" hover_color "#dce8f5"

            # 8. QUIT
            button:
                xsize 344
                ysize 46
                action Quit(confirm=True)
                activate_sound "audio/ui_cancel.wav"
                background None
                hover_background quit_hov
                padding (0, 0)
                at menu_item_reveal(0.28)
                fixed:
                    xfill True
                    yfill True
                    text "QUIT" xpos 20 yalign 0.5 size 20 font "fonts/lora_reg.ttf" kerning 3 color ("#d0ccf0" if tsuki_unlocked else "#b4c3d4") hover_color "#f0b4be"
                    if not is_ui_en():
                        text "退出" xpos 248 yalign 0.52 size 15 font "fonts/lxgw_xihei.ttf" color ("#a49ed4" if tsuki_unlocked else "#798ca2") hover_color "#e2a2ad"

            # Special Epilogue Postscript: 「月蝕」ECLIPSE (Full 5-Route Climax Story!)
            if tsuki_unlocked:
                null height 12
                add Solid("#dec89448", xsize=280, ysize=1) xpos 20
                null height 8

                button:
                    xsize 344
                    ysize 48
                    action [SetVariable("flowchart_target_node_id", "ext_07"), Start("flowchart_jump_dispatcher")]
                    background None
                    hover_background ecl_hov
                    padding (0, 0)
                    at menu_item_reveal(0.32)
                    fixed:
                        xfill True
                        yfill True
                        add "gui/mist/dot_gold.png" xpos 4 yalign 0.5
                        text "ECLIPSE" xpos 24 yalign 0.5 size 20 font "fonts/lora_reg.ttf" kerning 3.5 color "#ebd49a" hover_color "#fff6dc"
                        if not is_ui_en():
                            text "「月蝕」" xpos 238 yalign 0.52 size 15 font "fonts/lxgw_xihei_screen.ttf" color "#cbb378" hover_color "#fae7b8"

        text f"ENDINGS  {cleared_cnt} / 9   ·   CLASSIC HD v2.0":
            xpos 136
            yalign 0.945
            size 12
            color ("#a8a0cf" if tsuki_unlocked else "#73879e")
            font "fonts/lxgw_xihei.ttf"
            kerning 1.5


## ==============================================================================
## Floating Rounded Frosted-Mist Navigation Rail & Game Menu Shell (Exact Plan A!)
## ==============================================================================
screen navigation():
    # Floating Rounded Glass Sidebar Card (matching proposal_A_frosted_mist.jpg!)
    frame:
        xpos 28
        ypos 28
        xsize 306
        ysize 1024
        background Frame("gui/mist/rail.png", 26, 26)
        padding (0, 0)

        vbox:
            xpos 34
            ypos 38
            spacing 6

            text "月 姫" size 36 color "#eef4fa" font "fonts/lxgw_xihei_screen.ttf"
            text "CLASSIC HD" size 12 color "#7e92a8" font "fonts/lxgw_xihei.ttf" kerning 2.5

        vbox:
            xpos 20
            ypos 156
            spacing 6

            if not main_menu:
                $ nav_buttons = [
                    (ui_tr("返回物语", "Resume"),     Return(),                False, None),
                    (ui_tr("保存进度", "Save"),       ShowMenu("save"),        False, "save"),
                    (ui_tr("读取记录", "Load"),       ShowMenu("load"),        False, "load"),
                    (ui_tr("快捷读档", "Quick Load"), QuickLoad(),             False, None),
                    (ui_tr("物语图谱", "Flowchart"),  ShowMenu("flowchart"),   False, "flowchart"),
                    (ui_tr("画廊鉴赏", "Gallery"),    ShowMenu("cg_gallery"),  False, "cg_gallery"),
                    (ui_tr("音乐鉴赏", "Sound Test"), ShowMenu("music_room"),  False, "music_room"),
                    (ui_tr("文本履历", "History"),    ShowMenu("history"),     False, "history"),
                    (ui_tr("系统设置", "Config"),     ShowMenu("preferences"), False, "preferences"),
                    (ui_tr("操作说明", "Controls"),   ShowMenu("help"),        False, "help"),
                    (ui_tr("关于本作", "About"),      ShowMenu("about"),       False, "about"),
                    (ui_tr("标题画面", "Main Menu"),  MainMenu(),              False, None),
                    (ui_tr("退出游戏", "Quit"),       Quit(confirm=True),      True,  None),
                ]
            else:
                $ nav_buttons = [
                    (ui_tr("返回标题", "Back"),       Return(),                False, None),
                    (ui_tr("读取记录", "Load"),       ShowMenu("load"),        False, "load"),
                    (ui_tr("物语图谱", "Flowchart"),  ShowMenu("flowchart"),   False, "flowchart"),
                    (ui_tr("画廊鉴赏", "Gallery"),    ShowMenu("cg_gallery"),  False, "cg_gallery"),
                    (ui_tr("音乐鉴赏", "Sound Test"), ShowMenu("music_room"),  False, "music_room"),
                    (ui_tr("系统设置", "Config"),     ShowMenu("preferences"), False, "preferences"),
                    (ui_tr("操作说明", "Controls"),   ShowMenu("help"),        False, "help"),
                    (ui_tr("关于本作", "About"),      ShowMenu("about"),       False, "about"),
                    (ui_tr("退出游戏", "Quit"),       Quit(confirm=True),      True,  None),
                ]

            $ nav_sel_bg = Frame("gui/mist/nav_sel.png", 18, 16)
            $ nav_hov_bg = Frame("gui/mist/nav_hover.png", 18, 16)
            $ nav_rose_bg = Frame("gui/mist/nav_rose_hover.png", 18, 16)

            for zh_lbl, nact, is_quit, scr_tag in nav_buttons:
                $ is_cur_nav = bool(scr_tag and renpy.get_screen(scr_tag))
                button:
                    action nact
                    xsize 266
                    ysize 48
                    background (nav_sel_bg if is_cur_nav else None)
                    hover_background (nav_rose_bg if is_quit else (nav_sel_bg if is_cur_nav else nav_hov_bg))
                    padding (0, 0)

                    fixed:
                        xfill True
                        yfill True
                        if is_cur_nav:
                            add "gui/mist/dot_accent.png" xpos 18 yalign 0.5
                        text zh_lbl xpos (38 if is_cur_nav else 28) yalign 0.5 size 17 font ("fonts/lxgw_xihei_screen.ttf" if is_cur_nav else "fonts/lxgw_xihei.ttf") color ("#ffffff" if is_cur_nav else ("#b0becf" if is_quit else "#b2c1d3")) hover_color ("#f2b6c0" if is_quit else "#ffffff")


screen game_menu(title, scroll=None, subtitle=""):
    style_prefix "game_menu"

    # Pure Silky Frosted-Mist Ambient Backdrop (ZERO muddy blurred ghost!)
    add "gui/game_menu.webp"

    # Clean Airy Page Header (Right Canvas X=384)
    hbox:
        xpos 384
        ypos 50
        spacing 20
        text title size 32 color "#eef4fa" font "fonts/lxgw_xihei_screen.ttf" yalign 0.5
        if subtitle:
            text subtitle size 14 color "#7e92a8" font "fonts/lxgw_xihei.ttf" yalign 0.62

    frame:
        style "game_menu_outer_frame"

        hbox:
            frame:
                style "game_menu_navigation_frame"

            frame:
                style "game_menu_content_frame"

                if scroll == "viewport":
                    viewport:
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True
                        side_yfill True
                        vbox:
                            transclude
                elif scroll == "viewport_bottom":
                    viewport:
                        yinitial 1.0
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True
                        side_yfill True
                        vbox:
                            transclude
                elif scroll == "vpgrid":
                    vpgrid:
                        cols 1
                        yinitial 1.0
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True
                        side_yfill True
                        transclude
                else:
                    transclude

    use navigation

    if main_menu:
        key "game_menu" action ShowMenu("main_menu")


style game_menu_outer_frame is empty
style game_menu_navigation_frame is empty
style game_menu_content_frame is empty
style game_menu_viewport is gui_viewport
style game_menu_side is gui_side
style game_menu_scrollbar is gui_vscrollbar

style game_menu_outer_frame:
    top_padding 114
    bottom_padding 32

style game_menu_navigation_frame:
    xsize 384
    yfill True

style game_menu_content_frame:
    xsize 1484
    yfill True

style game_menu_viewport:
    xsize 1484

style game_menu_vscrollbar:
    unscrollable gui.unscrollable

style game_menu_side:
    spacing 12


## ==============================================================================
## Save & Load Screens - 3x2 Rounded Frosted Glass Archive Cards
## ==============================================================================
screen save():
    tag menu
    use file_slots(ui_tr("保存进度", "Save"), ui_tr("选择栏位保存当前阅读进度", "Select a slot to save progress"))

screen load():
    tag menu
    use file_slots(ui_tr("读取记录", "Load"), ui_tr("选择存档继续物语旅程", "Select a save slot to resume"))

screen file_slots(title, subtitle=""):
    use game_menu(title, subtitle=subtitle):
        fixed:
            xsize 1484
            ysize 920

            grid 3 2:
                xalign 0.5
                ypos 16
                spacing 34

                for i in range(6):
                    $ slot = i + 1

                    button:
                        action FileAction(slot)
                        xsize 452
                        ysize 322
                        background Frame("gui/mist/card.png", 24, 24)
                        hover_background Frame("gui/mist/card_sel.png", 24, 24)
                        padding (24, 20)

                        vbox:
                            spacing 12
                            xalign 0.5

                            frame:
                                xsize 404
                                ysize 229
                                background Solid("#0c1018")
                                padding (2, 2)

                                fixed:
                                    xfill True
                                    yfill True
                                    add Solid("#0d121b")
                                    text ui_tr("空栏位", "Empty") size 15 color "#526275" font "fonts/lxgw_xihei.ttf" xalign 0.5 yalign 0.5
                                    add FileScreenshot(slot) xalign 0.5 yalign 0.5

                            hbox:
                                xsize 404
                                text (f"Slot {slot:02d}" if is_ui_en() else f"存档 {slot:02d}") size 15 color "#a2c6e6" font "fonts/lxgw_xihei_screen.ttf" yalign 0.5
                                text FileTime(slot, format=_("{#file_time}%Y-%m-%d  %H:%M"), empty=ui_tr("尚未保存", "Empty")) size 13 color "#8b9db2" font "fonts/lxgw_xihei.ttf" xalign 1.0 yalign 0.5

                            text FileSaveName(slot) size 13 color "#d2deec" font "fonts/lxgw_xihei.ttf"

                        key "save_delete" action FileDelete(slot)

            # Soft Rounded Capsule Pagination Bar
            frame:
                xalign 0.5
                ypos 742
                background Frame("gui/mist/seg_track.png", 26, 22)
                padding (10, 6)

                hbox:
                    spacing 6

                    button:
                        action FilePagePrevious()
                        ysize 38
                        background None
                        hover_background Frame("gui/mist/pill_hover.png", 20, 16)
                        padding (16, 0)
                        text ui_tr("上一页", "Prev") size 14 color "#a8b9cc" hover_color "#ffffff" font "fonts/lxgw_xihei.ttf" yalign 0.5

                    if config.has_autosave:
                        button:
                            action FilePage("auto")
                            xsize 68
                            ysize 38
                            background None
                            hover_background Frame("gui/mist/pill_hover.png", 20, 16)
                            selected_background Frame("gui/mist/pill_active.png", 20, 16)
                            text ui_tr("自动", "Auto") size 14 color "#9fb0c4" hover_color "#ffffff" selected_color "#ffffff" font "fonts/lxgw_xihei.ttf" xalign 0.5 yalign 0.5

                    if config.has_quicksave:
                        button:
                            action FilePage("quick")
                            xsize 68
                            ysize 38
                            background None
                            hover_background Frame("gui/mist/pill_hover.png", 20, 16)
                            selected_background Frame("gui/mist/pill_active.png", 20, 16)
                            text ui_tr("快捷", "Quick") size 14 color "#9fb0c4" hover_color "#ffffff" selected_color "#ffffff" font "fonts/lxgw_xihei.ttf" xalign 0.5 yalign 0.5

                    for page in range(1, 10):
                        button:
                            action FilePage(page)
                            xsize 44
                            ysize 38
                            background None
                            hover_background Frame("gui/mist/pill_hover.png", 20, 16)
                            selected_background Frame("gui/mist/pill_active.png", 20, 16)
                            text f"{page:02d}" size 14 color "#9fb0c4" hover_color "#ffffff" selected_color "#ffffff" font "fonts/lxgw_xihei.ttf" xalign 0.5 yalign 0.5

                    button:
                        action FilePageNext()
                        ysize 38
                        background None
                        hover_background Frame("gui/mist/pill_hover.png", 20, 16)
                        padding (16, 0)
                        text ui_tr("下一页", "Next") size 14 color "#a8b9cc" hover_color "#ffffff" font "fonts/lxgw_xihei.ttf" yalign 0.5


## ==============================================================================
## Preferences Screen - Exact Plan A "Frosted Mist" (1:1 to Proposal A!)
## Soft Segmented Capsule Tabs + Rounded Glass Cards + Pill Toggle Switches
## ==============================================================================
screen preferences():
    tag menu

    default pref_tab = "display"

    $ bgm_pct = get_bgm_vol_pct()
    $ sfx_pct = get_sfx_vol_pct()
    $ cleared_cnt = get_cleared_endings_count()
    $ tsuki_ok = is_tsukishoku_unlocked()

    $ tab_defs = [
        ("display",  ui_tr("画面与演出", "Display")),
        ("reading",  ui_tr("阅读与字体", "Reading")),
        ("audio",    ui_tr("声音与快进", "Audio & Skip")),
        ("heroines", ui_tr("人物好感",   "Heroines")),
    ]
    $ is_en = is_ui_en()

    use game_menu(ui_tr("系统设置", "Config"), subtitle=ui_tr("显示、阅读与声音", "Display, reading & audio")):
        vbox:
            xsize 1444
            spacing 26

            # ------------------------------------------------------------------
            # Floating Capsule Segmented Tab Bar + Bilingual ZH / EN Toggle
            # ------------------------------------------------------------------
            hbox:
                xsize 1444
                frame:
                    xsize 760
                    ysize 54
                    background Frame("gui/mist/seg_track.png", 26, 22)
                    padding (6, 6)

                    hbox:
                        spacing 4
                        for tid, tlbl in tab_defs:
                            $ is_t = (pref_tab == tid)
                            button:
                                action SetScreenVariable("pref_tab", tid)
                                xsize 184
                                ysize 42
                                background (Frame("gui/mist/pill_active.png", 20, 16) if is_t else None)
                                hover_background (Frame("gui/mist/pill_active.png", 20, 16) if is_t else Frame("gui/mist/pill_hover.png", 20, 16))
                                text tlbl size 16 color ("#ffffff" if is_t else "#a8b8cb") font ("fonts/lxgw_xihei_screen.ttf" if is_t else "fonts/lxgw_xihei.ttf") xalign 0.5 yalign 0.5

                # Right-aligned UI Language Capsule Switcher (简体中文 | English)
                hbox:
                    xalign 1.0
                    yalign 0.5
                    spacing 12
                    text ui_tr("界面语言", "UI Language") size 13 color "#8294aa" font "fonts/lxgw_xihei.ttf" yalign 0.5
                    frame:
                        xsize 204
                        ysize 46
                        background Frame("gui/mist/seg_track.png", 22, 18)
                        padding (4, 4)
                        hbox:
                            spacing 4
                            button:
                                action SetField(persistent, "ui_lang", "zh")
                                xsize 96
                                ysize 38
                                background (Frame("gui/mist/pill_active.png", 18, 14) if not is_en else None)
                                hover_background (Frame("gui/mist/pill_active.png", 18, 14) if not is_en else Frame("gui/mist/pill_hover.png", 18, 14))
                                text "简体中文" size 13 color ("#ffffff" if not is_en else "#a4b5c8") font ("fonts/lxgw_xihei_screen.ttf" if not is_en else "fonts/lxgw_xihei.ttf") xalign 0.5 yalign 0.5
                            button:
                                action SetField(persistent, "ui_lang", "en")
                                xsize 96
                                ysize 38
                                background (Frame("gui/mist/pill_active.png", 18, 14) if is_en else None)
                                hover_background (Frame("gui/mist/pill_active.png", 18, 14) if is_en else Frame("gui/mist/pill_hover.png", 18, 14))
                                text "English" size 13 color ("#ffffff" if is_en else "#a4b5c8") font ("fonts/lxgw_xihei_screen.ttf" if is_en else "fonts/lxgw_xihei.ttf") xalign 0.5 yalign 0.5

            # ==================================================================
            # TAB 1: DISPLAY & STAGE FX (Exact 1:1 Proposal A Layout!)
            # ==================================================================
            if pref_tab == "display":
                vbox:
                    xsize 1444
                    spacing 24

                    # Card 1: Display Mode with Recessed Capsule Switch
                    frame:
                        xsize 1444
                        ysize 98
                        background Frame("gui/mist/card.png", 24, 24)
                        padding (32, 0)

                        hbox:
                            xfill True
                            yalign 0.5
                            vbox:
                                spacing 5
                                text ui_tr("显示模式", "Display Mode") size 18 color "#eef4fa" font "fonts/lxgw_xihei_screen.ttf"
                                text ui_tr("快捷键 Alt+Enter / F", "Shortcut: Alt+Enter / F") size 13 color "#8294aa" font "fonts/lxgw_xihei.ttf"

                            frame:
                                xalign 1.0
                                yalign 0.5
                                xsize 312
                                ysize 48
                                background Frame("gui/mist/seg_track.png", 24, 20)
                                padding (4, 4)

                                hbox:
                                    spacing 4
                                    button:
                                        action Preference("display", "window")
                                        xsize 150
                                        ysize 40
                                        background None
                                        hover_background Frame("gui/mist/pill_hover.png", 20, 16)
                                        selected_background Frame("gui/mist/pill_active.png", 20, 16)
                                        text ui_tr("窗口模式", "Window") size 15 color "#a4b5c8" hover_color "#ffffff" selected_color "#ffffff" font "fonts/lxgw_xihei.ttf" xalign 0.5 yalign 0.5
                                    button:
                                        action Preference("display", "fullscreen")
                                        xsize 150
                                        ysize 40
                                        background None
                                        hover_background Frame("gui/mist/pill_hover.png", 20, 16)
                                        selected_background Frame("gui/mist/pill_active.png", 20, 16)
                                        text ui_tr("全屏模式", "Fullscreen") size 15 color "#a4b5c8" hover_color "#ffffff" selected_color "#ffffff" font "fonts/lxgw_xihei.ttf" xalign 0.5 yalign 0.5

                    # Section 2: Aspect Ratio 3 Soft Rounded Schematic Cards
                    vbox:
                        spacing 14
                        hbox:
                            xpos 8
                            spacing 16
                            text ui_tr("画面比例", "Aspect Ratio") size 18 color "#eef4fa" font "fonts/lxgw_xihei_screen.ttf" yalign 0.5
                            text ui_tr("默认 4:3 柔焦边，完整保留原画", "Default 4:3 ambient framing preserves full artwork") size 13 color "#8294aa" font "fonts/lxgw_xihei.ttf" yalign 0.55

                        hbox:
                            spacing 24
                            for amode, sch_key, albl, adesc in [
                                ("4x3_ambient", "ambient", ui_tr("4:3 · 柔焦边", "4:3 · Ambient"), ui_tr("完整原画，两侧柔焦填充", "Full art with blurred sidebars")),
                                ("4x3_black",   "black",   ui_tr("4:3 · 纯黑边", "4:3 · Pillar"),  ui_tr("完整原画，两侧纯黑遮幅", "Full art with black sidebars")),
                                ("16x9_full",   "full",    ui_tr("16:9 · 满屏",  "16:9 · Full"),   ui_tr("铺满宽屏，自动顶偏裁切", "Widescreen fill with top crop")),
                            ]:
                                $ is_a = (persistent.aspect_mode == amode)
                                $ sch_img = f"gui/mist/sch_{sch_key}_sel.png" if is_a else f"gui/mist/sch_{sch_key}.png"
                                button:
                                    action [SetField(persistent, "aspect_mode", amode), Function(tsuki_refresh_stage)]
                                    xsize 465
                                    ysize 220
                                    background (Frame("gui/mist/card_sel.png", 24, 24) if is_a else Frame("gui/mist/card.png", 24, 24))
                                    hover_background (Frame("gui/mist/card_sel.png", 24, 24) if is_a else Frame("gui/mist/card_hover.png", 24, 24))
                                    padding (0, 0)

                                    vbox:
                                        xalign 0.5
                                        yalign 0.5
                                        spacing 14

                                        add sch_img xalign 0.5
                                        text albl size 17 color ("#ffffff" if is_a else "#c2d0e0") font "fonts/lxgw_xihei_screen.ttf" xalign 0.5
                                        text adesc size 13 color ("#a4bfd9" if is_a else "#7e90a6") font "fonts/lxgw_xihei.ttf" xalign 0.5

                    # Card 3: Grouped Frosted Panel for Stage FX Pill Toggle Switches
                    frame:
                        xsize 1444
                        ysize 206
                        background Frame("gui/mist/card.png", 24, 24)
                        padding (32, 8)

                        vbox:
                            xfill True
                            yalign 0.5
                            spacing 0

                            fixed:
                                xfill True
                                ysize 92
                                hbox:
                                    xfill True
                                    yalign 0.5
                                    vbox:
                                        spacing 5
                                        text ui_tr("环境光调色", "Ambient Sprite Tint") size 18 color "#eef4fa" font "fonts/lxgw_xihei_screen.ttf"
                                        text ui_tr("随场景时段调整立绘色调", "Adjust character tint to match scene time") size 13 color "#8294aa" font "fonts/lxgw_xihei.ttf"
                                    button:
                                        action [ToggleField(persistent, "enable_ambient_lighting"), Function(tsuki_refresh_stage)]
                                        xalign 1.0
                                        yalign 0.5
                                        background None
                                        padding (4, 4)
                                        add ("gui/mist/toggle_on.png" if persistent.enable_ambient_lighting else "gui/mist/toggle_off.png")

                            add Solid("#dce8f51a", xsize=1380, ysize=1)

                            fixed:
                                xfill True
                                ysize 92
                                hbox:
                                    xfill True
                                    yalign 0.5
                                    vbox:
                                        spacing 5
                                        text ui_tr("镜头微动", "Subtle Camera Motion") size 18 color "#eef4fa" font "fonts/lxgw_xihei_screen.ttf"
                                        text ui_tr("在 CG 与转场叠加微幅缓动", "Gentle camera drift on event CGs") size 13 color "#8294aa" font "fonts/lxgw_xihei.ttf"
                                    button:
                                        action [ToggleField(persistent, "enable_cinematic_motion"), Function(tsuki_refresh_stage)]
                                        xalign 1.0
                                        yalign 0.5
                                        background None
                                        padding (4, 4)
                                        add ("gui/mist/toggle_on.png" if persistent.enable_cinematic_motion else "gui/mist/toggle_off.png")

            # ==================================================================
            # TAB 2: READING & TYPOGRAPHY (Rounded Live NVL Preview + Soft Cards)
            # ==================================================================
            elif pref_tab == "reading":
                vbox:
                    xsize 1444
                    spacing 22

                    # Rounded Frosted Frame around Live NVL Preview Stage
                    frame:
                        xsize 1444
                        ysize 236
                        background Frame("gui/mist/card.png", 24, 24)
                        padding (12, 12)

                        fixed:
                            xsize 1420
                            ysize 212
                            if renpy.loadable("images/bg/bg_40d.webp"):
                                add Transform("images/bg/bg_40d.webp", crop=(0.0, 0.34, 1.0, 0.200), crop_relative=True, xysize=(1420, 212))
                            else:
                                add Solid("#121a28", xsize=1420, ysize=212)
                            add Transform(Solid("#060a12"), alpha=persistent.nvl_opacity, xsize=1420, ysize=212)

                            frame:
                                xpos 24
                                ypos 14
                                background Frame("gui/mist/quick_pill.png", 18, 12)
                                padding (14, 4)
                                text ui_tr("实时预览", "LIVE PREVIEW") size 12 color "#a2c6e6" font "fonts/lxgw_xihei.ttf"

                            vbox:
                                xpos 30
                                ypos 58
                                xsize 1350
                                spacing 10
                                text ui_tr("——啊，今晚的月色，竟然如此动人。", "—Ah, the moon is so beautiful tonight."):
                                    font get_story_font()
                                    size int(persistent.nvl_font_size)
                                    color "#eef4fa"
                                    outlines [(1, "#000000cc", 0, 1)]
                                text ui_tr("推开坡道尽头洋馆的铁门，夜风轻轻拂过被苍蓝月光照亮的庭院。", "Pushing open the iron gate at the top of the hill, a cool breeze drifts across the moonlit courtyard."):
                                    font get_story_font()
                                    size int(persistent.nvl_font_size)
                                    color "#eef4fa"
                                    outlines [(1, "#000000cc", 0, 1)]

                    # Story Font Selector (3 Rounded Frosted Cards)
                    vbox:
                        spacing 12
                        text ui_tr("正文字体", "Story Font") xpos 8 size 18 color "#eef4fa" font "fonts/lxgw_xihei_screen.ttf"
                        hbox:
                            spacing 22
                            for fkey, flbl, fdesc in [
                                ("song", ui_tr("思源宋体", "Noto Serif"),   ui_tr("明朝体风格，默认推荐", "Classic print serif (Default)")),
                                ("kai",  ui_tr("霞鹜文楷", "LXGW WenKai"),  ui_tr("楷书风格，观感柔和",   "Soft calligraphic style")),
                                ("sans", ui_tr("思源黑体", "Noto Sans"),    ui_tr("无衬线体，清晰利落",   "Clean modern sans-serif")),
                            ]:
                                $ is_f = (persistent.story_font == fkey)
                                button:
                                    action SetField(persistent, "story_font", fkey)
                                    xsize 466
                                    ysize 92
                                    background (Frame("gui/mist/card_sel.png", 24, 24) if is_f else Frame("gui/mist/card.png", 24, 24))
                                    hover_background (Frame("gui/mist/card_sel.png", 24, 24) if is_f else Frame("gui/mist/card_hover.png", 24, 24))
                                    padding (26, 0)
                                    vbox:
                                        yalign 0.5
                                        spacing 5
                                        text flbl size 19 color ("#ffffff" if is_f else "#ccd8e6") font STORY_FONT_MAP[fkey][0]
                                        text fdesc size 13 color ("#a4bfd9" if is_f else "#7e90a6") font "fonts/lxgw_xihei.ttf"

                    # Grouped Rounded Glass Card for 2x2 Smooth Circular-Thumb Sliders
                    frame:
                        xsize 1444
                        ysize 236
                        background Frame("gui/mist/card.png", 24, 24)
                        padding (34, 26)

                        hbox:
                            xfill True
                            yalign 0.5
                            spacing 76

                            vbox:
                                xsize 650
                                spacing 34

                                vbox:
                                    spacing 12
                                    hbox:
                                        xfill True
                                        text ui_tr("正文字号", "Font Size") size 16 color "#eef4fa" font "fonts/lxgw_xihei_screen.ttf"
                                        text f"{int(persistent.nvl_font_size)} px" size 16 color "#a2c6e6" font "fonts/lxgw_xihei_screen.ttf" xalign 1.0
                                    bar value FieldValue(persistent, "nvl_font_size", range=14, offset=26, step=1) xfill True

                                vbox:
                                    spacing 12
                                    hbox:
                                        xfill True
                                        text ui_tr("NVL 暗幕浓度", "NVL Veil Opacity") size 16 color "#eef4fa" font "fonts/lxgw_xihei_screen.ttf"
                                        text f"{int(round(persistent.nvl_opacity * 100))}%" size 16 color "#a2c6e6" font "fonts/lxgw_xihei_screen.ttf" xalign 1.0
                                    bar value FieldValue(persistent, "nvl_opacity", range=0.55, offset=0.35, step=0.02) xfill True

                            vbox:
                                xsize 650
                                spacing 34

                                vbox:
                                    spacing 12
                                    hbox:
                                        xfill True
                                        text ui_tr("文字显示速度", "Text Speed") size 16 color "#eef4fa" font "fonts/lxgw_xihei_screen.ttf"
                                        text ui_tr("最右侧即瞬间全显", "Rightmost = instant") size 13 color "#8294aa" font "fonts/lxgw_xihei.ttf" xalign 1.0 yalign 0.5
                                    bar value Preference("text speed") xfill True

                                vbox:
                                    spacing 12
                                    hbox:
                                        xfill True
                                        text ui_tr("自动阅读等待", "Auto-Forward Delay") size 16 color "#eef4fa" font "fonts/lxgw_xihei_screen.ttf"
                                        text ui_tr("控制 AUTO 翻页停顿", "Controls AUTO advance pace") size 13 color "#8294aa" font "fonts/lxgw_xihei.ttf" xalign 1.0 yalign 0.5
                                    bar value Preference("auto-forward time") xfill True

            # ==================================================================
            # TAB 3: AUDIO & SKIPPING (2 Calm Grouped Frosted Glass Cards)
            # ==================================================================
            elif pref_tab == "audio":
                vbox:
                    xsize 1444
                    spacing 26

                    # Card 1: Audio Mixer
                    frame:
                        xsize 1444
                        ysize 284
                        background Frame("gui/mist/card.png", 24, 24)
                        padding (34, 22)

                        vbox:
                            xfill True
                            yalign 0.5
                            spacing 24

                            vbox:
                                spacing 14
                                hbox:
                                    xfill True
                                    vbox:
                                        spacing 4
                                        text ui_tr("背景音乐（BGM）", "Music Volume (BGM)") size 18 color "#eef4fa" font "fonts/lxgw_xihei_screen.ttf"
                                        text ui_tr("2000 原版原声带", "2000 Original Soundtrack") size 13 color "#8294aa" font "fonts/lxgw_xihei.ttf"
                                    hbox:
                                        xalign 1.0
                                        yalign 0.5
                                        spacing 18
                                        text f"{bgm_pct}%" size 20 color "#a2c6e6" font "fonts/lxgw_xihei_screen.ttf" yalign 0.5 min_width 60
                                        button:
                                            action Preference("music mute", "toggle")
                                            xsize 112
                                            ysize 38
                                            background Frame("gui/mist/pill_idle.png", 20, 16)
                                            hover_background Frame("gui/mist/pill_hover.png", 20, 16)
                                            selected_background Frame("gui/mist/pill_rose.png", 20, 16)
                                            text ui_tr("静音", "Mute") size 14 color "#b8c7d8" hover_color "#ffffff" selected_color "#fae0e4" font "fonts/lxgw_xihei.ttf" xalign 0.5 yalign 0.5
                                bar value Preference("music volume") xfill True

                            add Solid("#dce8f51a", xsize=1376, ysize=1)

                            vbox:
                                spacing 14
                                hbox:
                                    xfill True
                                    vbox:
                                        spacing 4
                                        text ui_tr("音效音量（SFX）", "Sound Volume (SFX)") size 18 color "#eef4fa" font "fonts/lxgw_xihei_screen.ttf"
                                        text ui_tr("环境音效与界面按键音", "Ambient & UI sound effects") size 13 color "#8294aa" font "fonts/lxgw_xihei.ttf"
                                    hbox:
                                        xalign 1.0
                                        yalign 0.5
                                        spacing 18
                                        text f"{sfx_pct}%" size 20 color "#a2c6e6" font "fonts/lxgw_xihei_screen.ttf" yalign 0.5 min_width 60
                                        button:
                                            action Play("sound", "audio/ui_choice.wav")
                                            xsize 112
                                            ysize 38
                                            background Frame("gui/mist/pill_active.png", 20, 16)
                                            hover_background Frame("gui/mist/pill_hover.png", 20, 16)
                                            text ui_tr("试听音效", "Test SFX") size 14 color "#eef4fa" hover_color "#ffffff" font "fonts/lxgw_xihei.ttf" xalign 0.5 yalign 0.5
                                bar value Preference("sound volume") xfill True

                    # Card 2: Skipping Pill Switches
                    frame:
                        xsize 1444
                        ysize 206
                        background Frame("gui/mist/card.png", 24, 24)
                        padding (34, 8)

                        vbox:
                            xfill True
                            yalign 0.5
                            spacing 0

                            fixed:
                                xfill True
                                ysize 92
                                hbox:
                                    xfill True
                                    yalign 0.5
                                    vbox:
                                        spacing 5
                                        text ui_tr("允许快进未读文本", "Skip Unseen Text") size 18 color "#eef4fa" font "fonts/lxgw_xihei_screen.ttf"
                                        text ui_tr("开启后按住 Ctrl 或点击 SKIP 可快进未读剧情", "Allow Ctrl / SKIP to fast-forward unread lines") size 13 color "#8294aa" font "fonts/lxgw_xihei.ttf"
                                    button:
                                        action Preference("skip", "toggle")
                                        xalign 1.0
                                        yalign 0.5
                                        background None
                                        padding (4, 4)
                                        add ("gui/mist/toggle_on.png" if _preferences.skip_unseen else "gui/mist/toggle_off.png")

                            add Solid("#dce8f51a", xsize=1376, ysize=1)

                            fixed:
                                xfill True
                                ysize 92
                                hbox:
                                    xfill True
                                    yalign 0.5
                                    vbox:
                                        spacing 5
                                        text ui_tr("选择后继续快进", "Continue Skipping After Choices") size 18 color "#eef4fa" font "fonts/lxgw_xihei_screen.ttf"
                                        text ui_tr("做出选择支后保持快进状态", "Stay in skip mode after selecting a choice") size 13 color "#8294aa" font "fonts/lxgw_xihei.ttf"
                                    button:
                                        action Preference("after choices", "toggle")
                                        xalign 1.0
                                        yalign 0.5
                                        background None
                                        padding (4, 4)
                                        add ("gui/mist/toggle_on.png" if _preferences.skip_after_choices else "gui/mist/toggle_off.png")

            # ==================================================================
            # TAB 4: HEROINE PORTRAITS & LIVE AFFECTION (Plan 3: Near 2 + Far 3)
            # ==================================================================
            else:
                vbox:
                    xsize 1444
                    spacing 22

                    # Top Tier: Near Side (2 Wide Frosted Portrait Cards)
                    vbox:
                        spacing 12
                        hbox:
                            xpos 6
                            xsize 1432
                            text ui_tr("表线 · 近月篇（Near Side）", "Near Side of the Moon") size 16 color "#a2c6e6" font "fonts/lxgw_xihei_screen.ttf" yalign 0.5
                            text (ui_tr("当前周目好感度", "Current playthrough affection") if not main_menu else ui_tr("进入游戏后显示当前周目好感度", "Start or load a game to view live affection")) size 12 color "#7e90a6" font "fonts/lxgw_xihei.ttf" xalign 1.0 yalign 0.5

                        hbox:
                            spacing 28
                            for hkey, hzh, hen, hvar, hcol, hends in NEAR_HEROINE_PROFILES:
                                $ hval = 0 if main_menu else get_heroine_affection(hvar)
                                $ any_clr = any(is_ending_cleared(pv, sl) for pv, sl, _, _ in hends)
                                $ p_img = f"gui/portraits/{hkey}_warm.png" if (hval >= 6 or any_clr) else f"gui/portraits/{hkey}_norm.png"
                                $ bar_w = int(round(396 * min(1.0, hval / 15.0)))

                                frame:
                                    xsize 708
                                    ysize 332
                                    background Frame("gui/mist/card.png", 24, 24)
                                    padding (18, 18)

                                    hbox:
                                        spacing 26
                                        yalign 0.5

                                        frame:
                                            xsize 240
                                            ysize 292
                                            background Frame(f"gui/mist/pbox_{hkey}.png", 22, 22)
                                            padding (2, 2)
                                            add p_img xalign 0.5 yalign 0.5

                                        vbox:
                                            xsize 404
                                            yalign 0.5
                                            spacing 18

                                            hbox:
                                                xfill True
                                                vbox:
                                                    spacing 3
                                                    text (hen.title() if is_en else hzh) size 26 color "#eef4fa" font "fonts/lxgw_xihei_screen.ttf"
                                                    text (hzh if is_en else hen) size 12 color hcol font "fonts/lxgw_xihei.ttf" kerning 2
                                                text (f"{hval:02d}" if not main_menu else "—") size 42 color hcol font "fonts/lxgw_xihei_screen.ttf" xalign 1.0 yalign 0.5

                                            vbox:
                                                spacing 10
                                                hbox:
                                                    xfill True
                                                    text ui_tr("当前好感度", "Affection") size 13 color "#8b9db2" font "fonts/lxgw_xihei.ttf"
                                                    text (f"{hval} / 15" if not main_menu else ui_tr("未入周目", "In Menu")) size 12 color "#76899e" font "fonts/lxgw_xihei.ttf" xalign 1.0
                                                fixed:
                                                    xsize 396
                                                    ysize 10
                                                    add Frame("gui/mist/prog_track.png", 5, 0) xsize 396 ysize 10
                                                    if bar_w > 0:
                                                        add Frame(f"gui/mist/prog_{hkey}.png", 5, 0) xsize max(10, bar_w) ysize 10

                                            hbox:
                                                spacing 12
                                                for p_var, seen_lbl, elbl_zh, elbl_en in hends:
                                                    $ ok = is_ending_cleared(p_var, seen_lbl)
                                                    frame:
                                                        xsize 192
                                                        ysize 36
                                                        background (Frame(f"gui/mist/epill_{hkey}.png", 18, 14) if ok else Frame("gui/mist/pill_idle.png", 18, 14))
                                                        text ui_tr(elbl_zh, elbl_en) size 13 color ("#ffffff" if ok else "#7f92a8") font ("fonts/lxgw_xihei_screen.ttf" if ok else "fonts/lxgw_xihei.ttf") xalign 0.5 yalign 0.5

                    # Bottom Tier: Far Side (3 Balanced Frosted Portrait Cards)
                    vbox:
                        spacing 12
                        hbox:
                            xpos 6
                            xsize 1432
                            text ui_tr("里线 · 远月篇（Far Side）", "Far Side of the Moon") size 16 color "#d698a3" font "fonts/lxgw_xihei_screen.ttf" yalign 0.5
                            hbox:
                                xalign 1.0
                                yalign 0.5
                                spacing 18
                                text (f"Endings {cleared_cnt} / 9" if is_en else f"已达成结局 {cleared_cnt} / 9") size 13 color "#dec894" font "fonts/lxgw_xihei_screen.ttf" yalign 0.5
                                if tsuki_ok:
                                    text ui_tr("「月蝕」终章已解锁", "ECLIPSE Unlocked") size 13 color "#f5e4b4" font "fonts/lxgw_xihei_screen.ttf" yalign 0.5

                        hbox:
                            spacing 23
                            for hkey, hzh, hen, hvar, hcol, hends in FAR_HEROINE_PROFILES:
                                $ hval = 0 if main_menu else get_heroine_affection(hvar)
                                $ any_clr = any(is_ending_cleared(pv, sl) for pv, sl, _, _ in hends)
                                $ p_img = f"gui/portraits/{hkey}_warm.png" if (hval >= 6 or any_clr) else f"gui/portraits/{hkey}_norm.png"
                                $ bar_w = int(round(234 * min(1.0, hval / 15.0)))

                                frame:
                                    xsize 466
                                    ysize 356
                                    background Frame("gui/mist/card.png", 24, 24)
                                    padding (16, 18)

                                    hbox:
                                        spacing 18
                                        yalign 0.5

                                        frame:
                                            xsize 180
                                            ysize 316
                                            background Frame(f"gui/mist/pbox_{hkey}.png", 22, 22)
                                            padding (2, 6)
                                            add p_img xalign 0.5 yalign 0.5

                                        vbox:
                                            xsize 236
                                            yalign 0.5
                                            spacing 16

                                            vbox:
                                                spacing 2
                                                text (hen.title() if is_en else hzh) size 23 color "#eef4fa" font "fonts/lxgw_xihei_screen.ttf"
                                                text (hzh if is_en else hen) size 11 color hcol font "fonts/lxgw_xihei.ttf" kerning 2

                                            vbox:
                                                spacing 8
                                                hbox:
                                                    xfill True
                                                    text ui_tr("好感度", "Affection") size 13 color "#8b9db2" font "fonts/lxgw_xihei.ttf" yalign 0.65
                                                    text (f"{hval:02d}" if not main_menu else "—") size 36 color hcol font "fonts/lxgw_xihei_screen.ttf" xalign 1.0 yalign 0.5
                                                fixed:
                                                    xsize 234
                                                    ysize 10
                                                    add Frame("gui/mist/prog_track.png", 5, 0) xsize 234 ysize 10
                                                    if bar_w > 0:
                                                        add Frame(f"gui/mist/prog_{hkey}.png", 5, 0) xsize max(10, bar_w) ysize 10

                                            vbox:
                                                spacing 10
                                                for p_var, seen_lbl, elbl_zh, elbl_en in hends:
                                                    $ ok = is_ending_cleared(p_var, seen_lbl)
                                                    frame:
                                                        xsize 234
                                                        ysize 36
                                                        background (Frame(f"gui/mist/epill_{hkey}.png", 18, 14) if ok else Frame("gui/mist/pill_idle.png", 18, 14))
                                                        text ui_tr(elbl_zh, elbl_en) size 13 color ("#ffffff" if ok else "#7f92a8") font ("fonts/lxgw_xihei_screen.ttf" if ok else "fonts/lxgw_xihei.ttf") xalign 0.5 yalign 0.5
                                                if len(hends) == 1:
                                                    null height 36


## ==============================================================================
## History, Help & About Screens (Soft Rounded Frosted Mist Cards)
## ==============================================================================
screen history():
    tag menu
    predict False

    $ clean_hist = [renpy.filter_text_tags(h.what, allow=gui.history_allow_tags) for h in _history_list]
    $ clean_hist = [w for w in clean_hist if w and w.strip()]

    use game_menu(ui_tr("文本履历", "History"), scroll="viewport_bottom", subtitle=ui_tr("回溯已阅读的剧情文本", "Review recent dialogue lines")):
        if clean_hist:
            frame:
                xsize 1420
                background Frame("gui/mist/card.png", 24, 24)
                padding (36, 26)

                vbox:
                    xsize 1348
                    spacing 0

                    for hi, what in enumerate(clean_hist):
                        if hi > 0:
                            add Solid("#dce8f516", xsize=1348, ysize=1)
                        frame:
                            xfill True
                            background None
                            padding (0, 16)
                            text what:
                                substitute False
                                font get_story_font()
                                size 24
                                color "#e4edf7"
                                line_spacing 10
        else:
            text ui_tr("尚无阅读履历记录。", "No dialogue history yet.") size 18 color "#7f92a8" font "fonts/lxgw_xihei.ttf" xalign 0.5 yoffset 80

define gui.history_allow_tags = { "alt", "noalt", "rt", "rb", "art", "color" }


screen help():
    tag menu
    use game_menu(ui_tr("操作说明", "Controls"), scroll="viewport", subtitle=ui_tr("键盘与鼠标快捷交互", "Keyboard & mouse shortcuts")):
        frame:
            xsize 1420
            background Frame("gui/mist/card.png", 24, 24)
            padding (36, 20)

            vbox:
                xfill True
                spacing 0

                $ bindings = [
                    (ui_tr("左键 / Enter / Space", "Left Click / Enter / Space"), ui_tr("推进剧情、确认当前选择", "Advance dialogue or confirm")),
                    (ui_tr("右键 / Esc", "Right Click / Esc"), ui_tr("唤出游戏菜单 / 返回上一级界面", "Open game menu / go back")),
                    (ui_tr("滚轮向上 / PageUp", "Scroll Up / PageUp"), ui_tr("NVL 分页回溯历史对话（Rollback）", "Rollback previous NVL pages")),
                    (ui_tr("滚轮向下 / PageDown", "Scroll Down / PageDown"), ui_tr("向前回放已回溯文本", "Roll forward rolled-back text")),
                    (ui_tr("按住 Ctrl / Tab", "Hold Ctrl / Tab"), ui_tr("高速快进已读（或全部）文本", "Fast-forward read (or all) text")),
                    (ui_tr("H / 鼠标中键", "H / Middle Click"), ui_tr("隐藏全部文字界面，纯享原画与立绘", "Hide text UI to view artwork")),
                    (ui_tr("F / Alt + Enter", "F / Alt + Enter"), ui_tr("快速切换全屏 / 窗口模式", "Toggle Fullscreen / Windowed")),
                    ("S", ui_tr("保存当前画面高清截图", "Save screenshot")),
                    (ui_tr("画廊全屏：← / → / H", "Gallery Viewer: ← / → / H"), ui_tr("切换差分或上下张 CG，H 隐藏控制栏，Esc 关闭", "Switch variant/CG, H hides HUD, Esc closes")),
                ]

                for bi, (kname, kdesc) in enumerate(bindings):
                    if bi > 0:
                        add Solid("#dce8f518", xsize=1348, ysize=1)
                    fixed:
                        xfill True
                        ysize 66
                        hbox:
                            yalign 0.5
                            spacing 36
                            text kname size 15 color "#a2c6e6" font "fonts/lxgw_xihei_screen.ttf" min_width 280 yalign 0.5
                            text kdesc size 16 color "#e2ecf7" font "fonts/lxgw_xihei.ttf" yalign 0.5


screen about():
    tag menu
    use game_menu(ui_tr("关于本作", "About"), scroll="viewport", subtitle=ui_tr("版本与开源许可", "Version & open-source licenses")):
        frame:
            xsize 1420
            background Frame("gui/mist/card.png", 24, 24)
            padding (40, 32)

            vbox:
                xfill True
                spacing 22

                vbox:
                    spacing 6
                    text (f"TSUKIHIME  ~Classic HD~  v{config.version}" if is_ui_en() else f"月姬  ～Classic HD～  v{config.version}") size 30 color "#eef4fa" font "fonts/notoserif_sc.otf"
                    text "Blue Blue Glass Moon, Under The Crimson Air." size 17 color "#a2c6e6" font "fonts/lora_italic.ttf"

                add Solid("#dce8f51c", xsize=1340, ysize=1)

                vbox:
                    xfill True
                    spacing 0
                    $ credits_rows = [
                        (ui_tr("原作", "Original Work"), ui_tr("TYPE-MOON (2000) · 剧本：奈须蘑菇 / 原画：武内崇 / 音乐：KATE", "TYPE-MOON (2000) · Scenario: Kinoko Nasu / Art: Takashi Takeuchi / Music: KATE")),
                        (ui_tr("运行引擎", "Engine"), ui_tr(f"Ren'Py {renpy.version_only} · 非官方开源 BYOA 兼容层（MIT）", f"Ren'Py {renpy.version_only} · Unofficial Open-Source BYOA Engine (MIT)")),
                        (ui_tr("开源字库", "Open Fonts"), ui_tr("霞鹜新晰黑（IPA v1.0）、思源宋体 / 霞鹜文楷 / 思源黑体 / Lora（SIL OFL 1.1）", "LXGW Neo XiHei (IPA v1.0), Noto Serif / LXGW WenKai / Noto Sans / Lora (SIL OFL 1.1)")),
                        (ui_tr("资源来源", "Asset Source"), ui_tr("游戏图像、音频与剧本均由用户本地正版原盘导入", "All game art, audio, and scripts are imported locally from your own copy")),
                    ]
                    for ci, (role, val) in enumerate(credits_rows):
                        if ci > 0:
                            add Solid("#dce8f514", xsize=1340, ysize=1)
                        fixed:
                            xfill True
                            ysize 56
                            hbox:
                                yalign 0.5
                                spacing 36
                                text role size 15 color "#8ea2b8" font "fonts/lxgw_xihei_screen.ttf" min_width 160 yalign 0.5
                                text val size 15 color "#e4eef9" font "fonts/lxgw_xihei.ttf" yalign 0.5

                text ui_tr(
                    "本项目为非官方开源兼容引擎，与 TYPE-MOON 无关联；所有原作版权归 TYPE-MOON / Notes Co., Ltd. 所有。",
                    "Unofficial open-source compatibility engine unaffiliated with TYPE-MOON. All original work copyrights belong to TYPE-MOON / Notes Co., Ltd."
                ) size 13 color "#788aa0" font "fonts/lxgw_xihei.ttf"


## ==============================================================================
## Safe Confirm Modal - Soft Rounded Frosted Glass Dialog (NO Space/Enter Confirm!)
## ==============================================================================
init -1 python:
    CONFIRM_PROMPT_TRANSLATIONS = {
        "Are you sure you want to quit?": "确定要退出《月姬》吗？",
        "Are you sure you want to return to the main menu?\nThis will lose unsaved progress.": "确定要返回标题画面吗？\n未保存的游玩进度将会丢失。",
        "Are you sure you want to return to the main menu? This will lose unsaved progress.": "确定要返回标题画面吗？\n未保存的游玩进度将会丢失。",
        "Are you sure you want to return to the main menu?": "确定要返回标题画面吗？\n未保存的游玩进度将会丢失。",
        "Are you sure you want to overwrite your save?": "确定要覆盖当前存档记录吗？",
        "Loading will lose unsaved progress.\nAre you sure you want to do this?": "读取记录将丢失当前未保存进度，确定继续吗？",
        "Are you sure you want to delete this save?": "确定要永久删除这条存档记录吗？",
        "Are you sure you want to end the replay?": "确定要结束当前回放吗？",
    }

screen confirm(message, yes_action, no_action):
    modal True
    zorder 300

    add Solid("#070a12d6") at modal_backdrop_fade

    frame:
        xalign 0.5
        yalign 0.5
        xsize 660
        ysize 276
        background Frame("gui/mist/modal.png", 28, 28)
        padding (40, 34)
        at modal_editorial_in

        vbox:
            xalign 0.5
            yalign 0.5
            spacing 26

            hbox:
                xalign 0.5
                spacing 8
                add "gui/mist/dot_accent.png" yalign 0.5
                text ui_tr("操作确认", "Confirm") size 14 color "#a2c6e6" font "fonts/lxgw_xihei_screen.ttf" yalign 0.5

            $ confirm_text = message if is_ui_en() else CONFIRM_PROMPT_TRANSLATIONS.get(message, _(message))
            text confirm_text:
                size 20
                color "#eef4fa"
                font "fonts/lxgw_xihei.ttf"
                textalign 0.5
                xalign 0.5
                line_spacing 9

            hbox:
                xalign 0.5
                spacing 24

                button:
                    action yes_action
                    xsize 184
                    ysize 46
                    background Frame("gui/mist/pill_active.png", 20, 16)
                    hover_background Frame("gui/mist/pill_rose.png", 20, 16)
                    text ui_tr("确认", "Confirm") size 16 color "#ffffff" font "fonts/lxgw_xihei_screen.ttf" xalign 0.5 yalign 0.5

                button:
                    action no_action
                    activate_sound "audio/ui_cancel.wav"
                    xsize 184
                    ysize 46
                    background Frame("gui/mist/pill_idle.png", 20, 16)
                    hover_background Frame("gui/mist/pill_hover.png", 20, 16)
                    text ui_tr("取消", "Cancel") size 16 color "#c8d6e6" hover_color "#ffffff" font "fonts/lxgw_xihei.ttf" xalign 0.5 yalign 0.5

    key "game_menu" action no_action
    key "K_ESCAPE" action no_action


## ==============================================================================
## Soft Floating Skip Indicator & Notify Toast
## ==============================================================================
screen skip_indicator():
    zorder 100
    frame:
        xpos 24
        ypos gui.skip_ypos
        background Frame("gui/mist/quick_pill.png", 20, 16)
        padding (18, 7)
        hbox:
            spacing 8
            yalign 0.5
            add "gui/mist/dot_accent.png" yalign 0.5
            text ui_tr("快进中", "Skipping") size 14 color "#eef4fa" font "fonts/lxgw_xihei_screen.ttf" yalign 0.5
            text "▶" at delayed_blink(0.0, 0.9) size 10 color "#a2c6e6" font "fonts/notosans_med.otf" yalign 0.5
            text "▶" at delayed_blink(0.2, 0.9) size 10 color "#c4dcf2" font "fonts/notosans_med.otf" yalign 0.5
            text "▶" at delayed_blink(0.4, 0.9) size 10 color "#eef4fa" font "fonts/notosans_med.otf" yalign 0.5

transform delayed_blink(delay, cycle):
    alpha 0.30
    pause delay
    block:
        linear 0.18 alpha 1.0
        pause 0.18
        linear 0.18 alpha 0.30
        pause (cycle - 0.36)
        repeat

screen notify(message):
    zorder 100
    frame at notify_appear:
        xpos 24
        ypos gui.notify_ypos
        background Frame("gui/mist/quick_pill.png", 20, 16)
        padding (18, 8)
        hbox:
            spacing 10
            add "gui/mist/dot_accent.png" yalign 0.5
            text "[message!tq]" size 14 color "#eef4fa" font "fonts/lxgw_xihei.ttf" yalign 0.5
    timer 3.0 action Hide("notify")

transform notify_appear:
    on show:
        alpha 0
        linear 0.2 alpha 1.0
    on hide:
        linear 0.4 alpha 0.0
