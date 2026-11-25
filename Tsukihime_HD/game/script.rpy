## ==============================================================================
## Main Script Entrypoint - Tsukihime Classic HD (月姬 ～Classic HD～ v2.0)
## ==============================================================================

# Full-screen NVL Narrator (authentic Type-Moon literary prose presentation)
define n = Character(None, kind=nvl)

label start:
    $ persistent.execution_cnt += 1
    $ renpy.set_return_stack([])
    $ current_fc_node_id = "com_00"
    $ save_name = tsuki_format_save_name(get_flowchart_node("com_00"))
    $ quick_menu = True
    $ tsuki_reset_run_state()
    $ tsuki_clear_stage()
    nvl clear
    stop music fadeout 1.0
    stop ambient fadeout 0.8
    stop sound

    $ tsuki_solid("#000000", "crossfade_fst")

    # Play authentic Tsukihime 2000 Opening Poem Sequence
    call openning

    # Enter Day 1 Prologue & Full 5-Route Branching Tree
    jump f20
