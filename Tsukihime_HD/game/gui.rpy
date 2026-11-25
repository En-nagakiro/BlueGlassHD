## ==============================================================================
## GUI.rpy - Plan A "Frosted Mist" (薄雾琉璃) Soft Minimalist Design Tokens
## ==============================================================================

init offset = -2

init python:
    gui.init(1920, 1080)

define config.check_conflicting_properties = True

## Palette - Soft Frosted Slate-Blue, Mist Pearl & Restrained Dusty Rose
define gui.accent_color = '#a2c6e6'
define gui.idle_color = '#aebfd4'
define gui.idle_small_color = '#7c8ea4'
define gui.hover_color = '#eef3fa'
define gui.selected_color = '#ffffff'
define gui.insensitive_color = '#55647888'

define gui.muted_color = '#1e2636'
define gui.hover_muted_color = '#2c394f'

define gui.text_color = '#eef3fa'
define gui.interface_text_color = '#e8eff7'

## Typography - Slender Modern DengXian for UI + Literary Serif for NVL Prose
define gui.text_font = "fonts/notoserif_sc.otf"
define gui.name_text_font = "fonts/lxgw_xihei_screen.ttf"
define gui.interface_text_font = "fonts/lxgw_xihei.ttf"

define gui.text_size = 33
define gui.name_text_size = 32
define gui.interface_text_size = 18
define gui.label_text_size = 22
define gui.notify_text_size = 16
define gui.title_text_size = 34

## Backgrounds
define gui.main_menu_background = "gui/main_menu.webp"
define gui.game_menu_background = "gui/game_menu.webp"
define gui.main_menu_text_color = "#a2c6e6"

## ADV fallback dimensions
define gui.textbox_height = 240
define gui.textbox_yalign = 1.0
define gui.name_xpos = 200
define gui.name_ypos = -5
define gui.name_xalign = 0.0
define gui.namebox_width = None
define gui.namebox_height = None
define gui.namebox_borders = Borders(5, 5, 5, 5)
define gui.namebox_tile = False
define gui.dialogue_xpos = 200
define gui.dialogue_ypos = 45
define gui.dialogue_width = 1520
define gui.dialogue_text_xalign = 0.0

## Buttons
define gui.button_width = None
define gui.button_height = None
define gui.button_borders = Borders(0, 0, 0, 0)
define gui.button_tile = False
define gui.button_text_font = gui.interface_text_font
define gui.button_text_size = 16
define gui.button_text_idle_color = gui.idle_color
define gui.button_text_hover_color = gui.hover_color
define gui.button_text_selected_color = gui.selected_color
define gui.button_text_insensitive_color = gui.insensitive_color
define gui.button_text_xalign = 0.0

define gui.radio_button_borders = Borders(0, 0, 0, 0)
define gui.check_button_borders = Borders(0, 0, 0, 0)
define gui.confirm_button_text_xalign = 0.5
define gui.page_button_borders = Borders(8, 4, 8, 4)
define gui.quick_button_borders = Borders(6, 2, 6, 2)
define gui.quick_button_text_size = 13
define gui.quick_button_text_idle_color = "#96a8be"
define gui.quick_button_text_selected_color = "#eef4fa"

## Choices
define gui.choice_button_width = 1040
define gui.choice_button_height = 66
define gui.choice_button_tile = False
define gui.choice_button_borders = Borders(24, 10, 24, 10)
define gui.choice_button_text_font = gui.text_font
define gui.choice_button_text_size = 25
define gui.choice_button_text_xalign = 0.5
define gui.choice_button_text_idle_color = "#dce6f2"
define gui.choice_button_text_hover_color = "#ffffff"

## Save / Load Thumbnails
define config.thumbnail_width = 400
define config.thumbnail_height = 225
define gui.file_slot_cols = 3
define gui.file_slot_rows = 2
define gui.slot_spacing = 32

## Spacing & Frames
define gui.navigation_xpos = 64
define gui.skip_ypos = 20
define gui.notify_ypos = 58
define gui.choice_spacing = 16
define gui.navigation_spacing = 6
define gui.pref_spacing = 10
define gui.pref_button_spacing = 4
define gui.page_spacing = 6
define gui.main_menu_text_xalign = 0.0

define gui.frame_borders = Borders(0, 0, 0, 0)
define gui.confirm_frame_borders = Borders(0, 0, 0, 0)
define gui.skip_frame_borders = Borders(12, 6, 24, 6)
define gui.notify_frame_borders = Borders(16, 8, 24, 8)
define gui.frame_tile = False

## Smooth Rounded Bars & Scrollbars
define gui.bar_size = 22
define gui.scrollbar_size = 6
define gui.slider_size = 22
define gui.bar_tile = False
define gui.scrollbar_tile = False
define gui.slider_tile = False
define gui.bar_borders = Borders(0, 0, 0, 0)
define gui.scrollbar_borders = Borders(0, 0, 0, 0)
define gui.slider_borders = Borders(0, 0, 0, 0)
define gui.vbar_borders = Borders(0, 0, 0, 0)
define gui.vscrollbar_borders = Borders(0, 0, 0, 0)
define gui.vslider_borders = Borders(0, 0, 0, 0)
define gui.unscrollable = "hide"

## History & NVL
define gui.history_height = None
define gui.history_name_xpos = 140
define gui.history_name_ypos = 0
define gui.history_name_width = 140
define gui.history_name_xalign = 1.0
define gui.history_text_xpos = 0
define gui.history_text_ypos = 0
define gui.history_text_width = 1260
define gui.history_text_xalign = 0.0

define gui.nvl_borders = Borders(0, 0, 0, 0)
define gui.nvl_height = None
define gui.nvl_spacing = 14
define gui.nvl_name_xpos = 240
define gui.nvl_name_ypos = 0
define gui.nvl_name_width = 160
define gui.nvl_name_xalign = 1.0
define gui.nvl_text_xpos = 0
define gui.nvl_text_ypos = 0
define gui.nvl_text_width = 1180
define gui.nvl_text_xalign = 0.0
define gui.nvl_thought_xpos = 0
define gui.nvl_thought_ypos = 0
define gui.nvl_thought_width = 1180
define gui.nvl_thought_xalign = 0.0
define gui.nvl_button_xpos = 450
define gui.nvl_button_xalign = 0.0

define gui.language = "unicode"
