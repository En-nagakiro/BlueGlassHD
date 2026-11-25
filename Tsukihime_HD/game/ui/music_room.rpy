## ==============================================================================
## ui/music_room.rpy - Plan A "Frosted Mist" Sound Test (CD Booklet Glass Deck)
## Authentic 2000 Tsukihime 10-Track OST (KATE / EVER AFTER verified, Bilingual)
## ==============================================================================

init -1 python:
    music_player = MusicRoom(fadeout=0.8)
    MUSIC_ROOM_AVAILABLE = 0
    for _i in range(1, 11):
        _p = tsuki_bgm_path(_i)
        if _p:
            music_player.add(_p, always_unlocked=True)
            MUSIC_ROOM_AVAILABLE += 1

    OST_TRACKS = [
        ("01", "感情", "Feelings",            "馆・夜",   "Mansion · Night"),
        ("02", "灯火", "Lamplight",           "馆・朝",   "Mansion · Morning"),
        ("03", "日向", "Sunny Place",         "学校・昼", "School · Noon"),
        ("04", "幻舞", "Phantom Dance",       "传奇 I",   "Mystery I"),
        ("05", "訣別", "Farewell",            "终局",     "Finale"),
        ("06", "妖夏", "Strange Summer",      "传奇 II",  "Mystery II"),
        ("07", "望郷", "Nostalgia",           "追忆",     "Reminiscence"),
        ("08", "月姫", "Tsukihime",           "主题曲",   "Main Theme"),
        ("09", "月下", "Under the Moonlight", "主题变奏", "Theme Arrangement"),
        ("10", "ever after", "Ever After",    "片尾曲",   "Ending Theme"),
    ]

    def get_current_track_info():
        current = renpy.music.get_playing("music")
        for num, name_zh, name_en, desc_zh, desc_en in OST_TRACKS:
            path = tsuki_bgm_path(num)
            if path and current == path:
                return num, name_zh, name_en, ui_tr(desc_zh, desc_en), True
        return "08", "月姫", "Tsukihime", ui_tr("主题曲", "Main Theme"), False

    def get_music_vol_pct():
        try:
            return int(round(_preferences.get_mixer("music") * 100))
        except Exception:
            return 100


init -1:
    transform disc_rotate_playing:
        xanchor 0.5
        yanchor 0.5
        rotate 0
        linear 24.0 rotate 360
        repeat


screen music_room():
    tag menu

    $ cur_num, cur_zh, cur_en, cur_desc, is_any_playing = get_current_track_info()
    $ vol_pct = get_music_vol_pct()
    $ _ret_bgm = tsuki_bgm_path("08")
    $ has_bgm = (MUSIC_ROOM_AVAILABLE > 0)

    add "gui/game_menu.webp"

    # Airy Header
    hbox:
        xpos 76
        ypos 38
        xsize 1768

        hbox:
            spacing 16
            yalign 0.5
            text ui_tr("音乐鉴赏", "Sound Test") size 30 color "#eef4fa" font "fonts/lxgw_xihei_screen.ttf" yalign 0.5
            text ui_tr("2000 原版原声带 · KATE", "2000 Original Soundtrack · KATE") size 14 color "#8599b0" font "fonts/lxgw_xihei.ttf" yalign 0.58

        button:
            action [If(main_menu and _ret_bgm, Play("music", _ret_bgm, fadein=1.0)), Return()]
            xalign 1.0
            yalign 0.5
            ysize 40
            background Frame("gui/mist/pill_idle.png", 20, 16)
            hover_background Frame("gui/mist/pill_hover.png", 20, 16)
            padding (22, 0)
            text ui_tr("返回", "Back") size 14 color "#d6e2ef" hover_color "#ffffff" font "fonts/lxgw_xihei.ttf" yalign 0.5

    # Two Floating Soft Frosted Glass Cards
    hbox:
        xpos 76
        ypos 112
        spacing 32

        # Left Frosted Card: Soft Rounded Tracklist
        frame:
            xsize 1072
            ysize 900
            background Frame("gui/mist/card.png", 24, 24)
            padding (24, 22)

            viewport:
                xsize 1024
                ysize 856
                scrollbars "vertical"
                mousewheel True
                draggable True

                vbox:
                    xsize 1004
                    spacing 6

                    for num, name_zh, name_en, desc_zh, desc_en in OST_TRACKS:
                        $ path = tsuki_bgm_path(num)
                        $ is_curr = bool(path and renpy.music.get_playing("music") == path)

                        button:
                            action (music_player.Play(path) if path else None)
                            xfill True
                            ysize 78
                            background (Frame("gui/mist/nav_sel.png", 18, 16) if is_curr else None)
                            hover_background (Frame("gui/mist/nav_sel.png", 18, 16) if is_curr else Frame("gui/mist/nav_hover.png", 18, 16))
                            padding (22, 0)

                            fixed:
                                xfill True
                                yfill True

                                hbox:
                                    yalign 0.5
                                    spacing 22

                                    if is_curr:
                                        add "gui/mist/dot_accent.png" yalign 0.5
                                    else:
                                        text num size 16 color "#6a7d94" font "fonts/lxgw_xihei.ttf" min_width 28 yalign 0.5

                                    vbox:
                                        spacing 3
                                        yalign 0.5
                                        hbox:
                                            spacing 12
                                            text (name_en if is_ui_en() else f"「{name_zh}」") size 18 color ("#ffffff" if is_curr else "#dce6f2") font ("fonts/lxgw_xihei_screen.ttf" if is_curr else "fonts/lxgw_xihei.ttf") yalign 0.5
                                            text (f"「{name_zh}」" if is_ui_en() else name_en) size 13 color ("#a2c6e6" if is_curr else "#7a8da4") font "fonts/lxgw_xihei.ttf" yalign 0.56
                                        text ui_tr(desc_zh, desc_en) size 13 color ("#a8bdd4" if is_curr else "#6f8198") font "fonts/lxgw_xihei.ttf"

                                if is_curr:
                                    frame:
                                        xalign 0.98
                                        yalign 0.5
                                        background Frame("gui/mist/pill_active.png", 16, 12)
                                        padding (12, 4)
                                        text ui_tr("播放中", "Playing") size 12 color "#eef4fa" font "fonts/lxgw_xihei_screen.ttf"
                                elif not path:
                                    frame:
                                        xalign 0.98
                                        yalign 0.5
                                        background Frame("gui/mist/pill_idle.png", 16, 12)
                                        padding (12, 4)
                                        text ui_tr("未导入", "Missing") size 12 color "#6f8198" font "fonts/lxgw_xihei.ttf"

        # Right Frosted Card: Minimalist Vinyl Deck & Smooth Controls
        frame:
            xsize 664
            ysize 900
            background Frame("gui/mist/card.png", 24, 24)
            padding (40, 36)

            vbox:
                xalign 0.5
                yalign 0.5
                spacing 34

                fixed:
                    xsize 300
                    ysize 300
                    xalign 0.5

                    if is_any_playing:
                        add "gui/music_disc.png" at disc_rotate_playing:
                            xalign 0.5
                            yalign 0.5
                            zoom 0.58
                    else:
                        add "gui/music_disc.png":
                            xalign 0.5
                            yalign 0.5
                            zoom 0.58

                vbox:
                    xalign 0.5
                    spacing 8

                    text f"TRACK {cur_num}  ·  2000 OST" size 12 color "#8396ac" font "fonts/lxgw_xihei.ttf" kerning 2 xalign 0.5
                    text (cur_en if is_ui_en() else f"「{cur_zh}」") size 30 color "#eef4fa" font "fonts/lxgw_xihei_screen.ttf" xalign 0.5
                    text (f"「{cur_zh}」" if is_ui_en() else cur_en) size 15 color "#a2c6e6" font ("fonts/lxgw_xihei.ttf" if is_ui_en() else "fonts/lora_italic.ttf") xalign 0.5
                    text cur_desc size 14 color "#8b9db2" font "fonts/lxgw_xihei.ttf" xalign 0.5

                # Soft Capsule Transport Controls
                hbox:
                    xalign 0.5
                    spacing 18

                    button:
                        action (music_player.Previous() if has_bgm else None)
                        xsize 138
                        ysize 44
                        background Frame("gui/mist/pill_idle.png", 20, 16)
                        hover_background Frame("gui/mist/pill_hover.png", 20, 16)
                        text ui_tr("上一曲", "Prev") size 14 color ("#d6e2ef" if has_bgm else "#55667a") hover_color "#ffffff" font "fonts/lxgw_xihei.ttf" xalign 0.5 yalign 0.5

                    button:
                        action (music_player.Stop() if has_bgm else None)
                        xsize 138
                        ysize 44
                        background Frame("gui/mist/pill_idle.png", 20, 16)
                        hover_background Frame("gui/mist/pill_rose.png", 20, 16)
                        text ui_tr("停止", "Stop") size 14 color ("#d6e2ef" if has_bgm else "#55667a") hover_color "#fae0e4" font "fonts/lxgw_xihei.ttf" xalign 0.5 yalign 0.5

                    button:
                        action (music_player.Next() if has_bgm else None)
                        xsize 138
                        ysize 44
                        background Frame("gui/mist/pill_idle.png", 20, 16)
                        hover_background Frame("gui/mist/pill_hover.png", 20, 16)
                        text ui_tr("下一曲", "Next") size 14 color ("#d6e2ef" if has_bgm else "#55667a") hover_color "#ffffff" font "fonts/lxgw_xihei.ttf" xalign 0.5 yalign 0.5

                # Smooth Rounded Volume Slider
                vbox:
                    xalign 0.5
                    xsize 460
                    spacing 12

                    hbox:
                        xfill True
                        text ui_tr("播放音量", "Volume") size 14 color "#98abbe" font "fonts/lxgw_xihei.ttf"
                        text f"{vol_pct}%" size 14 color "#a2c6e6" font "fonts/lxgw_xihei_screen.ttf" xalign 1.0

                    bar value Preference("music volume") xalign 0.5 xsize 460

    key "K_ESCAPE" action [If(main_menu and _ret_bgm, Play("music", _ret_bgm, fadein=1.0)), Return()]
    key "game_menu" action [If(main_menu and _ret_bgm, Play("music", _ret_bgm, fadein=1.0)), Return()]
