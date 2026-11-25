## ==============================================================================
## ui/gallery.rpy - Plan A "Frosted Mist" Curated Museum CG Gallery
## Differential Grouping + Soft Rounded Glass Cards + 4:3 Zero-Crop Viewer
## ==============================================================================

init -1 python:
    import re as _gal_re

    GALLERY_DATA = {
        "arc": [
            'ark_e01', 'ark_e02', 'ark_e03', 'ark_e04', 'ark_e04b', 'ark_e05a', 'ark_e05b',
            'ark_e06a', 'ark_e06b', 'ark_e07', 'ark_e08', 'ark_e09', 'ark_e10',
            'ark_f01', 'ark_f02', 'ark_f03',
            'ark_h01', 'ark_h02', 'ark_h03', 'ark_h04', 'ark_h05', 'ark_h06', 'ark_h07',
            'ark_h08', 'ark_h09', 'ark_h10', 'ark_h10b', 'ark_h11', 'ark_h12', 'ark_h13',
        ],
        "ciel": [
            'cel_e01', 'cel_e02a', 'cel_e02b', 'cel_e03a', 'cel_e03b', 'cel_e04', 'cel_e05a',
            'cel_e05b', 'cel_e06a', 'cel_e06b', 'cel_e07a', 'cel_e07b', 'cel_e07c', 'cel_e08',
            'cel_e09', 'cel_f01', 'cel_f01b', 'cel_f02',
            'cel_h01', 'cel_h02', 'cel_h03a', 'cel_h03b', 'cel_h04a', 'cel_h04b', 'cel_h05a',
            'cel_h05b', 'cel_h06a', 'cel_h06b', 'cel_h07a', 'cel_h07b', 'cel_h08a', 'cel_h08b',
            'cel_h09a', 'cel_h09b', 'cel_h10', 'cel_h11a', 'cel_h11b',
        ],
        "akiha": [
            'aki_e01', 'aki_e01b', 'aki_e02', 'aki_e03', 'aki_e04', 'aki_e04b', 'aki_e05a',
            'aki_e05b', 'aki_e06', 'aki_e07a', 'aki_e07b', 'aki_e08', 'aki_e09',
            'aki_f01', 'aki_f02',
            'aki_h01', 'aki_h02', 'aki_h03', 'aki_h04', 'aki_h05', 'aki_h06', 'aki_h07',
            'aki_h08', 'aki_h09', 'aki_h10', 'aki_h11', 'aki_h12', 'aki_h13', 'aki_h14', 'aki_h15',
        ],
        "hisui": [
            'his_e01', 'his_e01b', 'his_e02', 'his_e02b', 'his_e02b2', 'his_e03', 'his_e04',
            'his_e05', 'his_e06', 'his_e07a', 'his_e07b', 'his_e08', 'his_e09',
            'his_f01', 'his_f02', 'his_f03',
            'his_h01', 'his_h02', 'his_h03', 'his_h04a', 'his_h04b', 'his_h05', 'his_h06',
            'his_h06b', 'his_h07', 'his_h08', 'his_h09', 'his_h10', 'his_h11', 'his_h12',
            'his_h13', 'his_h14', 'his_h15', 'his_h16',
        ],
        "kohaku": [
            'koha_e01a', 'koha_e01b', 'koha_e02', 'koha_e03', 'koha_e04', 'koha_e05',
            'koha_e06', 'koha_e07', 'koha_e08',
            'koha_f01', 'koha_f01b', 'koha_f02', 'koha_f03',
            'koha_h01', 'koha_h02', 'koha_h03', 'koha_h04', 'koha_h05', 'koha_h06a',
            'koha_h06b', 'koha_h07', 'koha_h08', 'koha_h10', 'koha_h10b', 'koha_h11',
        ],
        "others": [
            'ao_01', 'ao_02', 'hal_e01', 'nero_e04',
            'stk_e01a', 'stk_e01b', 'stk_e01c', 'stk_e01d', 'stk_e02', 'stk_e03',
            'cmo_01', 'cmo_02', 'cmo_03', 'cmo_04a', 'cmo_04b', 'cmo_05', 'cmo_05b',
            'cmo_06', 'cmo_06b', 'cmo_07', 'cmo_08', 'cmo_09', 'cmo_10', 'cmo_11',
            'cmo_12', 'cmo_13', 'cmo_14', 'cmo_15', 'cmo_16', 'cmo_17', 'cmo_18',
            'cmo_19', 'cmo_20',
        ],
    }

    GALLERY_DATA["all"] = []
    for _k in ("arc", "ciel", "akiha", "hisui", "kohaku", "others"):
        GALLERY_DATA["all"].extend(GALLERY_DATA[_k])

    # Soft Morandi-pastel route accents (zero harsh neon!)
    GALLERY_CAT_META = [
        ("all",    "全部典藏",   "#a2c6e6", "ALL ARCHIVE"),
        ("arc",    "爱尔奎特",   "#dec894", "ARCUEID"),
        ("ciel",   "希耶尔",     "#98c2e2", "CIEL"),
        ("akiha",  "远野秋叶",   "#d698a3", "AKIHA"),
        ("hisui",  "翡翠",       "#9ac9cf", "HISUI"),
        ("kohaku", "琥珀",       "#ddb692", "KOHAKU"),
        ("others", "回忆与特写", "#aab8c9", "MEMORIES"),
    ]

    GALLERY_CAT_LOOKUP = {c[0]: c for c in GALLERY_CAT_META}

    def gallery_image_path(cname):
        if cname.startswith("cmo_"):
            return f"images/bg/{cname}.webp"
        return f"images/cg/{cname}.webp"

    def gallery_cg_label(base_name):
        if base_name.startswith("ark_f"):  return ui_tr("爱尔奎特 · 终章插画", "Arcueid · Epilogue")
        if base_name.startswith("ark_h"):  return ui_tr("爱尔奎特 · 亲密事件", "Arcueid · Intimate")
        if base_name.startswith("ark_"):   return ui_tr("爱尔奎特 · 剧情插画", "Arcueid · Event")
        if base_name.startswith("cel_f"):  return ui_tr("希耶尔 · 终章插画",   "Ciel · Epilogue")
        if base_name.startswith("cel_h"):  return ui_tr("希耶尔 · 亲密事件",   "Ciel · Intimate")
        if base_name.startswith("cel_"):   return ui_tr("希耶尔 · 剧情插画",   "Ciel · Event")
        if base_name.startswith("aki_f"):  return ui_tr("远野秋叶 · 终章插画", "Akiha · Epilogue")
        if base_name.startswith("aki_h"):  return ui_tr("远野秋叶 · 亲密事件", "Akiha · Intimate")
        if base_name.startswith("aki_"):   return ui_tr("远野秋叶 · 剧情插画", "Akiha · Event")
        if base_name.startswith("his_f"):  return ui_tr("翡翠 · 终章插画",     "Hisui · Epilogue")
        if base_name.startswith("his_h"):  return ui_tr("翡翠 · 亲密事件",     "Hisui · Intimate")
        if base_name.startswith("his_"):   return ui_tr("翡翠 · 剧情插画",     "Hisui · Event")
        if base_name.startswith("koha_f"): return ui_tr("琥珀 · 终章插画",     "Kohaku · Epilogue")
        if base_name.startswith("koha_h"): return ui_tr("琥珀 · 亲密事件",     "Kohaku · Intimate")
        if base_name.startswith("koha_"):  return ui_tr("琥珀 · 剧情插画",     "Kohaku · Event")
        if base_name.startswith("ao_"):    return ui_tr("苍崎青子 · 草原约定", "Aoko · Promise")
        if base_name.startswith("nero_"):  return ui_tr("尼禄·卡欧斯 · 混沌之兽", "Nrvnqsr · Chaos")
        if base_name.startswith("stk_"):   return ui_tr("弓塚五月 · 悲叹之夜", "Satsuki · Night")
        if base_name.startswith("hal_"):   return ui_tr("远野志贵 · 异变瞬间", "Shiki · Vision")
        if base_name.startswith("cmo_"):   return ui_tr("记忆特写 · 命运残片", "Memory · Fragment")
        return ui_tr("原画典藏", "Artwork")

    def is_cg_unlocked(cname):
        if persistent.unlock_all_routes:
            return True
        seen_set = getattr(persistent, "seen_cgs", None)
        if seen_set and cname in seen_set:
            return True
        if cname.startswith("cmo_"):
            return renpy.seen_image(f"bg {cname}")
        return renpy.seen_image(f"cg {cname}")

    def build_gallery_groups(cat):
        raw = GALLERY_DATA.get(cat, [])
        groups = []
        idx_map = {}
        for cname in raw:
            base = _gal_re.sub(r"(\d+)[a-z]\d*$", r"\1", cname)
            if base not in idx_map:
                idx_map[base] = len(groups)
                groups.append({"base": base, "label": gallery_cg_label(base), "variants": [cname]})
            else:
                groups[idx_map[base]]["variants"].append(cname)
        return groups

    GALLERY_GROUPS = {k: build_gallery_groups(k) for k in GALLERY_DATA}

    def get_gallery_stats(cat):
        items = GALLERY_DATA.get(cat, [])
        u = sum(1 for c in items if is_cg_unlocked(c))
        total_all = len(GALLERY_DATA["all"])
        u_all = sum(1 for c in GALLERY_DATA["all"] if is_cg_unlocked(c))
        pct = int(round(u * 100.0 / len(items))) if items else 0
        return u, len(items), pct, u_all, total_all

    def get_unlocked_scene_groups(cat):
        out = []
        for g in GALLERY_GROUPS.get(cat, []):
            uv = [v for v in g["variants"] if is_cg_unlocked(v)]
            if uv:
                out.append({"base": g["base"], "label": g["label"], "variants": uv})
        return out


screen cg_gallery():
    tag menu

    default current_cat = "all"
    default current_page = 0

    $ cat_id, cat_name, accent_col, cat_en = GALLERY_CAT_LOOKUP.get(current_cat, GALLERY_CAT_META[0])
    $ groups = GALLERY_GROUPS.get(current_cat, [])
    $ unlocked_scenes = get_unlocked_scene_groups(current_cat)
    $ cat_u, cat_t, cat_pct, all_u, all_t = get_gallery_stats(current_cat)
    $ items_per_page = 8
    $ total_pages = max(1, (len(groups) + items_per_page - 1) // items_per_page)
    $ safe_page = min(current_page, total_pages - 1)
    $ page_start = safe_page * items_per_page
    $ page_groups = groups[page_start : page_start + items_per_page]
    $ prog_w = int(round(196 * (cat_pct / 100.0)))

    # Pure Silky Frosted Mist Backdrop (Zero ghost blobs!)
    add "gui/game_menu.webp"

    # Airy Header Bar
    hbox:
        xpos 76
        ypos 38
        xsize 1768

        hbox:
            spacing 16
            yalign 0.5
            text ui_tr("画廊鉴赏", "CG Gallery") size 30 color "#eef4fa" font "fonts/lxgw_xihei_screen.ttf" yalign 0.5
            text (cat_en if is_ui_en() else f"{cat_name}  ·  {cat_en}") size 14 color accent_col font "fonts/lxgw_xihei.ttf" yalign 0.58

        hbox:
            xalign 1.0
            yalign 0.5
            spacing 16

            button:
                id "gal_return_btn"
                action Return()
                ysize 40
                background Frame("gui/mist/pill_idle.png", 20, 16)
                hover_background Frame("gui/mist/pill_hover.png", 20, 16)
                padding (22, 0)
                text ui_tr("返回", "Back") size 14 color "#d6e2ef" hover_color "#ffffff" font "fonts/lxgw_xihei.ttf" yalign 0.5

    # Soft Capsule Category Switcher + Progress Pill
    hbox:
        xpos 76
        ypos 96
        xsize 1768

        frame:
            background Frame("gui/mist/seg_track.png", 26, 22)
            padding (6, 5)
            hbox:
                spacing 4
                for cid, clbl, ccol, cen in GALLERY_CAT_META:
                    $ is_act = (current_cat == cid)
                    button:
                        action [SetScreenVariable("current_cat", cid), SetScreenVariable("current_page", 0)]
                        ysize 38
                        background (Frame("gui/mist/pill_active.png", 20, 16) if is_act else None)
                        hover_background (Frame("gui/mist/pill_active.png", 20, 16) if is_act else Frame("gui/mist/pill_hover.png", 20, 16))
                        padding (20, 0)
                        text ui_tr(clbl, cen.title()) size 14 color ("#ffffff" if is_act else "#a4b5c8") font ("fonts/lxgw_xihei_screen.ttf" if is_act else "fonts/lxgw_xihei.ttf") yalign 0.5

        hbox:
            xalign 1.0
            yalign 0.5
            spacing 16
            text (f"Section {cat_u} / {cat_t} ({cat_pct}%)" if is_ui_en() else f"当前分区 {cat_u} / {cat_t}（{cat_pct}%）") size 13 color "#a4b6ca" font "fonts/lxgw_xihei.ttf" yalign 0.5
            fixed:
                xsize 196
                ysize 8
                yalign 0.5
                add Frame("gui/slider/hairline_track.png", 4, 0) xsize 196 ysize 22 yalign 0.5
                if prog_w > 6:
                    add Frame("gui/slider/hairline_fill.png", 4, 0) xsize prog_w ysize 22 yalign 0.5

    # Curated 4 x 2 Soft Rounded Frosted Glass Cards
    grid 4 2:
        xpos 76
        ypos 166
        xsize 1768
        ysize 784
        spacing 26

        for local_i, grp in enumerate(page_groups):
            $ scene_no = page_start + local_i + 1
            $ variants = grp["variants"]
            $ unlocked_vars = [v for v in variants if is_cg_unlocked(v)]
            $ is_u = bool(unlocked_vars)
            $ thumb_path = gallery_image_path(unlocked_vars[0]) if is_u else None
            $ total_v = len(variants)
            $ got_v = len(unlocked_vars)
            $ all_got = (got_v == total_v)
            $ scene_idx = next((idx for idx, sg in enumerate(unlocked_scenes) if sg["base"] == grp["base"]), 0) if is_u else 0

            button:
                id f"gal_card_{local_i}"
                xsize 422
                ysize 376
                action (Show("cg_viewer", scene_list=unlocked_scenes, start_scene_idx=scene_idx) if is_u else None)
                background Frame("gui/mist/card.png", 24, 24)
                hover_background (Frame("gui/mist/card_sel.png", 24, 24) if is_u else Frame("gui/mist/card.png", 24, 24))
                padding (15, 14)

                vbox:
                    spacing 12
                    xalign 0.5

                    # 4:3 Artwork Viewport (392x294)
                    fixed:
                        xsize 392
                        ysize 294
                        add Solid("#0c1018", xsize=392, ysize=294)

                        if is_u:
                            add Transform(thumb_path, xysize=(392, 294)) xalign 0.5 yalign 0.5

                            if total_v > 1:
                                frame:
                                    xalign 0.96
                                    ypos 10
                                    background Frame("gui/mist/quick_pill.png", 16, 12)
                                    padding (12, 4)
                                    hbox:
                                        spacing 6
                                        add ("gui/mist/dot_gold.png" if all_got else "gui/mist/dot_accent.png") yalign 0.5
                                        text (f"{got_v}/{total_v}" if is_ui_en() else f"{got_v}/{total_v} 差分") size 12 color ("#f5e4b4" if all_got else "#e4eef8") font "fonts/lxgw_xihei_screen.ttf"
                        else:
                            vbox:
                                xalign 0.5
                                yalign 0.5
                                spacing 10
                                add Transform("gui/icons/lock.png", zoom=0.70) xalign 0.5
                                text ui_tr("未收录原画", "Locked") size 13 color "#627488" font "fonts/lxgw_xihei.ttf" xalign 0.5

                    hbox:
                        xsize 392
                        text f"NO.{scene_no:02d}  {gallery_cg_label(grp['base'])}" size 14 color ("#e6eef8" if is_u else "#627488") font "fonts/lxgw_xihei.ttf" yalign 0.5
                        if is_u:
                            text (ui_tr("全差分", "Complete") if (total_v > 1 and all_got) else (ui_tr("浏览", "View") if total_v == 1 else (f"{got_v}/{total_v}" if is_ui_en() else f"已收 {got_v}/{total_v}"))) size 12 color (accent_col if all_got else "#90a4ba") font "fonts/lxgw_xihei_screen.ttf" xalign 1.0 yalign 0.5

        for _i in range(8 - len(page_groups)):
            null

    # Soft Capsule Pagination Bar
    frame:
        xalign 0.5
        ypos 984
        background Frame("gui/mist/seg_track.png", 26, 22)
        padding (10, 6)

        hbox:
            spacing 20
            yalign 0.5

            if safe_page > 0:
                button:
                    action SetScreenVariable("current_page", safe_page - 1)
                    ysize 38
                    background Frame("gui/mist/pill_idle.png", 20, 16)
                    hover_background Frame("gui/mist/pill_hover.png", 20, 16)
                    padding (20, 0)
                    text ui_tr("上一页", "Prev") size 14 color "#dce6f2" hover_color "#ffffff" font "fonts/lxgw_xihei.ttf" yalign 0.5
            else:
                frame:
                    ysize 38
                    padding (20, 0)
                    text ui_tr("上一页", "Prev") size 14 color "#4f6074" font "fonts/lxgw_xihei.ttf" yalign 0.5

            text (f"Page {safe_page + 1:02d} / {total_pages:02d}   ·   {len(groups)} Scenes ({all_u}/{all_t} Variants)" if is_ui_en() else f"第 {safe_page + 1:02d} 页 / 共 {total_pages:02d} 页   ·   {len(groups)} 组精选插画（{all_u}/{all_t} 差分）") size 14 color "#c4d2e2" font "fonts/lxgw_xihei.ttf" yalign 0.5

            if safe_page < total_pages - 1:
                button:
                    action SetScreenVariable("current_page", safe_page + 1)
                    ysize 38
                    background Frame("gui/mist/pill_idle.png", 20, 16)
                    hover_background Frame("gui/mist/pill_hover.png", 20, 16)
                    padding (20, 0)
                    text ui_tr("下一页", "Next") size 14 color "#dce6f2" hover_color "#ffffff" font "fonts/lxgw_xihei.ttf" yalign 0.5
            else:
                frame:
                    ysize 38
                    padding (20, 0)
                    text ui_tr("下一页", "Next") size 14 color "#4f6074" font "fonts/lxgw_xihei.ttf" yalign 0.5

    key "K_ESCAPE" action Return()
    key "game_menu" action Return()


## ==============================================================================
## Fullscreen 4:3 Zero-Crop CG Viewer with Soft Frosted Capsule HUD
## ==============================================================================
screen cg_viewer(scene_list, start_scene_idx=0):
    zorder 200
    modal True

    default s_idx = start_scene_idx
    default v_idx = 0
    default show_hud = True

    $ total_s = max(1, len(scene_list))
    $ safe_s = max(0, min(s_idx, total_s - 1))
    $ cur_scene = scene_list[safe_s]
    $ cur_vars = cur_scene["variants"]
    $ total_v = max(1, len(cur_vars))
    $ safe_v = max(0, min(v_idx, total_v - 1))
    $ cur_name = cur_vars[safe_v]
    $ cur_path = gallery_image_path(cur_name)

    $ next_s = safe_s if (safe_v + 1 < total_v) else ((safe_s + 1) % total_s)
    $ next_v = (safe_v + 1) if (safe_v + 1 < total_v) else 0
    $ prev_s = safe_s if (safe_v > 0) else ((safe_s - 1) % total_s)
    $ prev_v = (safe_v - 1) if (safe_v > 0) else (len(scene_list[(safe_s - 1) % total_s]["variants"]) - 1)

    add Solid("#060910")
    add Transform(cur_path, xysize=(1920, 1440), xalign=0.5, yalign=0.5, blur=48.0, matrixcolor=BrightnessMatrix(-0.56) * SaturationMatrix(0.45))
    add Transform(cur_path, xysize=(1440, 1080), xalign=0.5, yalign=0.5)

    button:
        xfill True
        yfill True
        background None
        action [SetScreenVariable("s_idx", next_s), SetScreenVariable("v_idx", next_v)]

    if show_hud:
        frame:
            xalign 0.5
            yalign 0.972
            background Frame("gui/mist/quick_pill.png", 20, 16)
            padding (22, 8)

            hbox:
                spacing 20
                yalign 0.5

                button:
                    action [SetScreenVariable("s_idx", prev_s), SetScreenVariable("v_idx", prev_v)]
                    background None
                    hover_background Frame("gui/mist/pill_hover.png", 16, 12)
                    padding (12, 4)
                    text ui_tr("上一张", "Prev") size 13 color "#c8d6e6" hover_color "#ffffff" font "fonts/lxgw_xihei.ttf"

                text f"{gallery_cg_label(cur_scene['base'])}  ·  {safe_s + 1:02d}/{total_s:02d}" size 14 color "#eef4fa" font "fonts/lxgw_xihei_screen.ttf" yalign 0.5

                if total_v > 1:
                    hbox:
                        spacing 6
                        yalign 0.5
                        text ui_tr("差分", "Var") size 12 color "#8ea2b8" font "fonts/lxgw_xihei.ttf" yalign 0.5
                        for vi in range(total_v):
                            $ is_cur_v = (vi == safe_v)
                            button:
                                action SetScreenVariable("v_idx", vi)
                                background (Frame("gui/mist/pill_active.png", 14, 10) if is_cur_v else Frame("gui/mist/pill_idle.png", 14, 10))
                                hover_background Frame("gui/mist/pill_hover.png", 14, 10)
                                padding (10, 3)
                                text f"{vi + 1:02d}" size 12 color ("#ffffff" if is_cur_v else "#a4b6ca") font "fonts/lxgw_xihei_screen.ttf"

                button:
                    action [SetScreenVariable("s_idx", next_s), SetScreenVariable("v_idx", next_v)]
                    background None
                    hover_background Frame("gui/mist/pill_hover.png", 16, 12)
                    padding (12, 4)
                    text ui_tr("下一张", "Next") size 13 color "#c8d6e6" hover_color "#ffffff" font "fonts/lxgw_xihei.ttf"

                button:
                    action ToggleScreenVariable("show_hud")
                    background None
                    hover_background Frame("gui/mist/pill_hover.png", 16, 12)
                    padding (12, 4)
                    text ui_tr("隐藏栏 (H)", "Hide (H)") size 13 color "#92a5ba" hover_color "#ffffff" font "fonts/lxgw_xihei.ttf"

                button:
                    action Hide("cg_viewer")
                    background None
                    hover_background Frame("gui/mist/pill_rose.png", 16, 12)
                    padding (12, 4)
                    text ui_tr("关闭", "Close") size 13 color "#e8b0ba" hover_color "#ffffff" font "fonts/lxgw_xihei_screen.ttf"

    key "K_ESCAPE" action Hide("cg_viewer")
    key "game_menu" action Hide("cg_viewer")
    key "K_h" action ToggleScreenVariable("show_hud")
    key "K_LEFT" action [SetScreenVariable("s_idx", prev_s), SetScreenVariable("v_idx", prev_v)]
    key "K_RIGHT" action [SetScreenVariable("s_idx", next_s), SetScreenVariable("v_idx", next_v)]
