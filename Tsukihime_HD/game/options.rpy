## ==============================================================================
## Options.rpy - Core Engine Configuration (Blue Glass Engine / Classic HD v2.0)
## ==============================================================================

init -1 python:
    # Dedicated looping ambient channel for NScripter `waveloop` (rain, cicadas, heartbeats)
    renpy.music.register_channel("ambient", mixer="sfx", loop=True, tight=True)

init -1:
    define config.name = _("月姬 ～Classic HD～")
    define gui.show_name = False
    define config.version = "2.0.1"
    define gui.about = _("非官方开源 BYOA 兼容引擎（MIT）")
    define build.name = "BlueGlassHD"

    define config.has_sound = True
    define config.has_music = True
    define config.has_voice = False

    # Title music is resolved dynamically at init 0 below via tsuki_bgm_path("08")
    # so splashscreen -> main_menu hands off seamlessly without Ren'Py calling music.stop(),
    # while empty BYOA packages still keep config.main_menu_music = None.

    define config.enter_transition = Dissolve(0.25)
    define config.exit_transition = Dissolve(0.25)
    define config.intra_transition = Dissolve(0.22)
    define config.after_load_transition = Dissolve(0.35)
    define config.end_game_transition = Dissolve(0.5)
    define config.window_show_transition = Dissolve(0.18)
    define config.window_hide_transition = Dissolve(0.18)

    define config.window = "auto"
    # Keep save_directory stable across upgrades so existing player saves persist cleanly
    define config.save_directory = "Tsukihime_HD_v2"
    define config.window_icon = "gui/window_icon.png"

    # Authentic NVL Paged Rollback & Modern Tactile Reading Feel
    default preferences.fullscreen = True
    default preferences.text_cps = 55
    default preferences.afm_time = 15
    define config.nvl_paged_rollback = True
    define config.nvl_list_length = 24
    define config.rollback_enabled = True
    define config.rollback_length = 200
    define config.history_length = 400
    define config.fast_skipping = True
    define config.allow_skipping = True
    define config.hard_rollback_limit = 200
    define config.autosave_on_choice = True
    define config.autosave_on_quit = True

init python:
    # Dynamically bind main_menu_music when Track 08 is imported so 00start.rpy keeps
    # splashscreen music playing seamlessly (if_changed=True) instead of stopping it.
    _mm_bgm_init = tsuki_bgm_path("08")
    if _mm_bgm_init:
        config.main_menu_music = _mm_bgm_init
        config.main_menu_music_fadein = 1.5

    # Standard exclusions
    build.classify('**~', None)
    build.classify('**.bak', None)
    build.classify('**/.**', None)
    build.classify('**/#**', None)
    build.classify('**/thumbs.db', None)
    build.classify('**/_smoke_test.*', None)
    build.classify('README.md', None)
    build.classify('log.txt', None)
    build.classify('traceback.txt', None)

    # Hard BYOA Compliance Guard: NEVER pack user-imported original/derived assets or saves!
    build.classify('game/images/**', None)
    build.classify('game/story/**', None)
    build.classify('game/saves/**', None)
    build.classify('game/cache/**', None)
    build.classify('game/gui/portraits/**', None)
    build.classify('game/gui/main_menu.webp', None)
    build.classify('game/gui/title_eclipse_moon.png', None)
    build.classify('game/gui/title_eclipse_kanji.png', None)
    build.classify('game/core/story_variables.rpy*', None)
    build.classify('game/core/image_definitions.rpy*', None)
    build.classify('game/core/byoa_meta.rpy*', None)
    build.classify('game/audio/0*', None)
    build.classify('game/audio/1*', None)
    build.classify('game/audio/se_*', None)
