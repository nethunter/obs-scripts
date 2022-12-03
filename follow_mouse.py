"""
This script is intended to be called from OBS Studio. Provides
mouse-based zoom and tracking for macOS desktop sources.
For more information please visit:
"""

description = (
    "Crops and resizes a source to simulate a zoomed in tracked to"\
    " the mouse.\n\n"
    + "Set activation hotkey in Settings.\n\n"
    + "Active Border enables lazy/smooth tracking; border size"\
    "calculated as percent of smallest dimension. "
    + "Border of 50% keeps mouse locked in the center of the zoom"\
    " frame\n\n"
    + "By David Tabachnikov (@hml / @davidtab)\n\n"
)

import obspython as obs 
import pywinctl as pwc # version >=0.0.38
from pprint import pformat
from platform import system
import math
import time
from json import load, loads

c = pwc.getMousePos
get_position = lambda: [c().x, c().y]
ZOOM_NAME_TOG = "zoom.toggle"
FOLLOW_NAME_TOG = "follow.toggle"
ZOOM_DESC_TOG = "Enable/Disable Mouse Zoom"
FOLLOW_DESC_TOG = "Enable/Disable Mouse Follow"

class CursorFollow:
    flag = lock = track = update = False
    scene_item = current_scene_as_source = None
    bounds = obs.vec2()

    def init_scene(self) -> None:
        self.current_scene_as_source = obs.obs_frontend_get_current_scene()
        if self.current_scene_as_source:
            current_scene = obs.obs_scene_from_source(self.current_scene_as_source)
            self.scene_item = obs.obs_scene_find_source_recursive(current_scene, "Screen")
            obs.obs_sceneitem_get_bounds(self.scene_item, self.bounds)
    
    def tick(self, seconds):
            crop = obs.obs_sceneitem_crop()
            pos = get_position()

            if self.scene_item and self.lock:
                crop.left = int(pos[0])
                crop.right = int((self.bounds.x/2) - pos[0])
                crop.top = int(pos[1])
                crop.bottom = int((self.bounds.y/2) - pos[1])

            obs.obs_sceneitem_set_crop(self.scene_item, crop)
            obs.obs_source_release(self.current_scene_as_source)

zoom = CursorFollow()

def script_description():
    return description

def script_load(settings):
    zoom_id_tog = obs.obs_hotkey_register_frontend(
        ZOOM_NAME_TOG, ZOOM_DESC_TOG, toggle_zoom
    )
    hotkey_save_array = obs.obs_data_get_array(settings, ZOOM_NAME_TOG)
    obs.obs_hotkey_load(zoom_id_tog, hotkey_save_array)
    obs.obs_data_array_release(hotkey_save_array)

    zoom.init_scene()

def toggle_zoom(pressed):
    if pressed:
        zoom.lock = not zoom.lock

def script_tick(seconds):
    zoom.tick(seconds)
