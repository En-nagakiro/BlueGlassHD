## ==============================================================================
## ui/byoa_gate.rpy - First-Run BYOA Asset Setup Screen (Bilingual ZH / EN)
## Shown cleanly when launched from an open-source release before importing assets
## ==============================================================================

screen byoa_setup_required():
    tag menu
    add "gui/game_menu.webp"

    $ byoa_st = get_byoa_status()
    $ is_en = is_ui_en()

    frame:
        xalign 0.5
        yalign 0.5
        xsize 980
        background Frame("gui/mist/card.png", 24, 24)
        padding (44, 38)

        vbox:
            spacing 22
            xfill True

            hbox:
                xfill True
                vbox:
                    spacing 6
                    text ui_tr("BYOA  ·  资源未导入", "BYOA  ·  ASSETS NOT IMPORTED") size 13 color "#a2c6e6" font "fonts/lxgw_xihei_screen.ttf" kerning 2
                    text ui_tr("请先从本地原版《月姬 (2000)》导入游戏文件", "Import Assets From Your Local Tsukihime (2000) Copy") size 26 color "#eef4fa" font "fonts/lxgw_xihei_screen.ttf"

                hbox:
                    xalign 1.0
                    yalign 0.5
                    spacing 12

                    # Bilingual ZH / EN instant switcher
                    frame:
                        background Frame("gui/mist/seg_track.png", 18, 14)
                        padding (3, 3)
                        hbox:
                            spacing 2
                            button:
                                action SetField(persistent, "ui_lang", "zh")
                                xsize 58
                                ysize 30
                                background (Frame("gui/mist/pill_active.png", 14, 10) if not is_en else None)
                                hover_background (Frame("gui/mist/pill_active.png", 14, 10) if not is_en else Frame("gui/mist/pill_hover.png", 14, 10))
                                text "中文" size 12 color ("#ffffff" if not is_en else "#9ab0c8") font "fonts/lxgw_xihei_screen.ttf" xalign 0.5 yalign 0.5
                            button:
                                action SetField(persistent, "ui_lang", "en")
                                xsize 58
                                ysize 30
                                background (Frame("gui/mist/pill_active.png", 14, 10) if is_en else None)
                                hover_background (Frame("gui/mist/pill_active.png", 14, 10) if is_en else Frame("gui/mist/pill_hover.png", 14, 10))
                                text "EN" size 12 color ("#ffffff" if is_en else "#9ab0c8") font "fonts/lxgw_xihei_screen.ttf" xalign 0.5 yalign 0.5

                    frame:
                        yalign 0.5
                        background Frame("gui/mist/pill_idle.png", 20, 14)
                        padding (14, 6)
                        text ui_tr("仅含开源引擎", "ENGINE ONLY") size 12 color "#c6d6e8" font "fonts/lxgw_xihei.ttf"

            add Solid("#dce8f51c", xsize=892, ysize=1)

            text ui_tr(
                "本发行包不含任何原版图像、音频与剧本。运行导入工具指向你的原版目录（支持日文原盘、月箱、汉化版或英化版）即可本地构建：",
                "This package contains no copyrighted art, audio, or script. Point the importer to your legally owned Tsukihime (2000) folder (JP / Tsukibako / CN / EN) to build locally:"
            ) size 15 color "#b8c7d8" font "fonts/lxgw_xihei.ttf" line_spacing 6

            frame:
                xfill True
                background Frame("gui/mist/seg_track.png", 20, 18)
                padding (24, 18)

                vbox:
                    spacing 10
                    for k, lbl_zh, lbl_en, desc_zh, desc_en in [
                        ("story",     "剧本（game/story/）",           "Script (game/story/)",           "支持 0.txt 与 nscript.dat，自动识别编码", "Supports 0.txt & nscript.dat with auto encoding"),
                        ("images",    "图像（game/images/）",          "Images (game/images/)",          "支持 arc.nsa / arc.sar 与散装目录",        "Supports arc.nsa / arc.sar or unpacked image/"),
                        ("title_art", "标题图（game/gui/）",           "Title Art (game/gui/)",          "从原版 title1.jpg 本地合成",               "Synthesized locally from original title1.jpg"),
                        ("portraits", "角色肖像（game/gui/portraits/）", "Portraits (game/gui/portraits/)", "从解包立绘本地裁切生成",                   "Cropped locally from extracted standing sprites"),
                        ("audio",     "音乐与音效（game/audio/，可选）", "Audio & BGM (game/audio/, opt.)", "支持 WAV / FLAC / OGG / MP3",             "Supports WAV / FLAC / OGG / MP3"),
                    ]:
                        $ ok = byoa_st.get(k, False)
                        fixed:
                            xfill True
                            ysize 28
                            add ("gui/mist/dot_mint.png" if ok else "gui/mist/dot_dim.png") xpos 0 yalign 0.5
                            text ui_tr(lbl_zh, lbl_en) xpos 24 yalign 0.5 size 14 color ("#e8f8f0" if ok else "#d4e0ee") font "fonts/lxgw_xihei_screen.ttf"
                            text ui_tr(desc_zh, desc_en) xpos 330 yalign 0.5 size 13 color "#8496ab" font "fonts/lxgw_xihei.ttf"
                            text (ui_tr("已就绪", "Ready") if ok else ui_tr("缺失", "Missing")) xalign 1.0 yalign 0.5 size 13 color ("#8ee6c6" if ok else "#e0a2ac") font "fonts/lxgw_xihei_screen.ttf"

            frame:
                xfill True
                background Frame("gui/mist/card.png", 18, 18)
                padding (22, 16)
                vbox:
                    spacing 6
                    text ui_tr("导入方式：", "How to import:") size 13 color "#8ea2b8" font "fonts/lxgw_xihei.ttf"
                    text ui_tr(
                        "1. 双击同目录下的 BYOA_Importer.exe，选择原版《月姬》目录一键导入（免装 Python）",
                        "1. Launch BYOA_Importer.exe in this folder and select your Tsukihime (2000) directory (no Python needed)"
                    ) size 15 color "#eef4fa" font "fonts/lxgw_xihei_screen.ttf"
                    text ui_tr(
                        "2. 开发者命令行：pwsh -File import_assets.ps1 -Source \"<原版目录>\"",
                        "2. CLI (developers): pwsh -File import_assets.ps1 -Source \"<Tsukihime_Dir>\""
                    ) size 13 color "#9fb2c8" font "fonts/lxgw_xihei.ttf"

            hbox:
                xalign 1.0
                spacing 14
                button:
                    action Function(renpy.reload_script)
                    ysize 42
                    background Frame("gui/mist/pill_active.png", 20, 16)
                    hover_background Frame("gui/mist/pill_hover.png", 20, 16)
                    padding (24, 0)
                    text ui_tr("重新检测", "Re-check") size 14 color "#ffffff" font "fonts/lxgw_xihei_screen.ttf" yalign 0.5

                button:
                    action Quit(confirm=False)
                    ysize 42
                    background Frame("gui/mist/pill_idle.png", 20, 16)
                    hover_background Frame("gui/mist/pill_rose.png", 20, 16)
                    padding (24, 0)
                    text ui_tr("退出", "Quit") size 14 color "#d0dce8" hover_color "#ffffff" font "fonts/lxgw_xihei.ttf" yalign 0.5

    key "K_ESCAPE" action NullAction()
    key "game_menu" action NullAction()
