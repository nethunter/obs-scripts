"""
This script is intended to be called from OBS Studio. Provides
mouse-based zoom and tracking for macOS desktop sources.
For more information please visit:
"""

import obspython as obs 
import pywinctl as pwc
from enum import Enum
from utils.hotkey import Hotkey

class ZoomFollowStates(Enum):
    FOLLOW = 1
    WINDOW = 2
    RECT = 3

"""
Main class for the script - all the actual logic is here
"""
class ZoomFollow:
    scene_item = current_scene_as_source = None
    mode = "none"
    hotkeys = []
    
    bounds = obs.vec2()
    crop = obs.obs_sceneitem_crop()
    rect = obs.vec4()


    def load(self, settings):
        current_scene_as_source = obs.obs_frontend_get_current_scene()
        if current_scene_as_source:
            current_scene = obs.obs_scene_from_source(current_scene_as_source)
            scene_item = obs.obs_scene_find_source_recursive(current_scene, "Screen")
            obs.obs_sceneitem_get_bounds(scene_item, self.bounds)
            obs.obs_source_release(current_scene_as_source)

            self.scene_item = scene_item
            
        self.init_hotkeys(settings)

    def init_hotkeys(self, settings):
        def set_follow(pressed):
            if pressed:
                self.set_mode(ZoomFollowStates.FOLLOW)

        def set_rect(pressed):
            if pressed:
                print("Pressed hotkey 2")

        def set_window(pressed):
            if pressed:
                print("Pressed hotkey 3")

        def reset(pressed):
            if pressed:
                print("Reset")

        self.hotkeys = [
            Hotkey(set_follow, settings, "zf.follow.toggle", "ZoomFollow: Follow mouse"),
            Hotkey(set_rect, settings, "zf.rect.set", "ZoomFollow: Set rectangle"),
            Hotkey(set_window, settings, "zf.window.set", "ZoomFollow: Zoom to active window"),
            Hotkey(reset, settings, "zf.zoom.reset", "ZoomFollow: Reset")
        ]

    def save(self, settings):
        for htk in self.hotkeys:
            htk.save_hotkey()

    def set_mode(self, mode):
        print(f"Switching mode to {mode}")
        self.mode = mode

    def tick(self, seconds):
        if not self.scene_item:
            return

        match self.mode:
            case ZoomFollowStates.FOLLOW:
                pos = pwc.getMousePos()
                crop.left = int(pos.x)
                crop.right = int((self.bounds.x/2) - pos.x)
                crop.top = int(pos.y)
                crop.bottom = int((self.bounds.y/2) - pos.y)

        obs.obs_sceneitem_set_crop(self.scene_item, crop)

zf = ZoomFollow()

"""
Script definitions
"""
def script_description():
    return (
        "Zooms into the screen and has a few modes of following:\n"
        + "Follow mouse, lock window, lock region\n\n"
        + "By David Tabachnikov (@hml / @davidtab)\n\n"
    )

def script_load(settings):
    zf.load(settings)

def script_save(settings):
    zf.save(settings)

def script_tick(seconds):
    zf.tick(seconds)