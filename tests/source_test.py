import obspython as obs
import pywinctl as pwc

def obs_displays():
    current_scene_as_source = obs.obs_frontend_get_current_scene()
    current_scene = obs.obs_scene_from_source(current_scene_as_source)
    scene_item = obs.obs_scene_find_source_recursive(current_scene, "Screen")
    source = obs.obs_sceneitem_get_source(scene_item)
    settings = obs.obs_source_get_settings(source)
    display = obs.obs_data_get_int(settings, "display")
    print(f"{display}")

def pywinctl_displays():
    monitors = pwc.getAllScreens()
    for monitor in monitors.items():
        print(f"Monitor ID {monitor}")

def script_load(settings):
    obs_displays()
    pywinctl_displays()