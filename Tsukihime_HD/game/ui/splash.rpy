## ==============================================================================
## ui/splash.rpy - Two-Beat Editorial Opening Ident (BYOA Compliant)
## ==============================================================================

init -1:
    transform splash_brand_pulse:
        alpha 0.0 yoffset 6
        easein 0.9 alpha 1.0 yoffset 0
        pause 1.4
        easeout 0.8 alpha 0.0 yoffset -3

    transform splash_quote_reveal:
        alpha 0.0 yoffset 6
        easein 1.2 alpha 1.0 yoffset 0
        pause 1.9
        easeout 0.9 alpha 0.0 yoffset -4

label splashscreen:
    if not is_byoa_assets_installed():
        return

    scene black with None
    $ renpy.pause(0.22)

    # 1. Minimalist Open-Source Engine Ident
    show expression Text("{size=34}{color=#eef3f9}{font=fonts/lora_reg.ttf}B L U E   G L A S S   M O O N{/font}{/color}{/size}\n\n{size=13}{color=#7c90a8}{font=fonts/lora_italic.ttf}Classic HD Compatibility Engine{/font}{/color}{/size}", text_align=0.5) as splash_ident at splash_brand_pulse:
        xalign 0.5
        yalign 0.5
    $ renpy.pause(3.1)
    hide splash_ident

    $ renpy.pause(0.20)

    # 2. Title Theme swells in with locally imported opening epigraph (core/byoa_meta.rpy)
    $ _title_bgm = tsuki_bgm_path("08")
    if _title_bgm:
        $ renpy.music.play(_title_bgm, channel="music", loop=True, fadein=2.2, if_changed=True)

    if BYOA_SPLASH_QUOTE:
        $ _sub_block = f"\n\n{{size=15}}{{color=#7b92ac}}{{font=fonts/lora_italic.ttf}}{BYOA_SPLASH_SUB}{{/font}}{{/color}}{{/size}}" if BYOA_SPLASH_SUB else ""
        show expression Text(f"{{size=32}}{{color=#dce8f5}}{{font=fonts/notoserif_sc.otf}}{BYOA_SPLASH_QUOTE}{{/font}}{{/color}}{{/size}}{_sub_block}", text_align=0.5) as splash_quote at splash_quote_reveal:
            xalign 0.5
            yalign 0.5
        $ renpy.pause(4.0)
        hide splash_quote
        $ renpy.pause(0.22)

    return
