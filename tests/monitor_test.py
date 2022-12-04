import obspython as obs 
import pywinctl as pwc

monitor = None

def update_loc():
    global monitor

    pos = pwc.getMousePos()
    monitor_pos = monitor[1]['pos']
    monitor_size = monitor[1]['size']
    in_x = (pos.x - monitor_pos.x >= 0 and pos.x - monitor_pos.x <= monitor_size.width)
    in_y = (pos.y + monitor_pos.y >= 0 and pos.y + monitor_pos.y <= monitor_size.height)
    #print(f"Monitor ID {monitor}")
    print(f"Mouse: {monitor[0]}, {pos.x - monitor_pos.x}, {in_x}, {pos.y + monitor_pos.y}, {in_y}")

def get_obs_display():
    current_scene_as_source = obs.obs_frontend_get_current_scene()
    current_scene = obs.obs_scene_from_source(current_scene_as_source)
    scene_item = obs.obs_scene_find_source_recursive(current_scene, "Screen")
    source = obs.obs_sceneitem_get_source(scene_item)
    settings = obs.obs_source_get_settings(source)
    display = obs.obs_data_get_int(settings, "display")
    print(f"{display}")
    return display

def script_load(settings):
    global monitor
    obs_display = get_obs_display()

    for monitor_src in pwc.getAllScreens().items():
        if monitor_src[1]['id'] == obs_display:
            print(f"Found monitor {monitor_src[0]}")
            monitor = monitor_src

    obs.timer_add(update_loc, 3000)