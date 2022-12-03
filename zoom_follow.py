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
    NONE = 1
    FOLLOW = 2
    WINDOW = 3
    RECT = 4

"""
Main class for the script - all the actual logic is here
"""
class ZoomFollow:
    scene_item = current_scene_as_source = None
    mode = "none"
    hotkeys = []
    
    crop = obs.obs_sceneitem_crop()
    target_crop = obs.obs_sceneitem_crop()
    source_size = obs.vec2()
    rect = None
    screen = None

    def load(self, settings):
        current_scene_as_source = obs.obs_frontend_get_current_scene()

        if not current_scene_as_source:
            return

        current_scene = obs.obs_scene_from_source(current_scene_as_source)
        self.scene_item = obs.obs_scene_find_source_recursive(current_scene, "Screen")
        source = obs.obs_sceneitem_get_source(self.scene_item)
        source_settings = obs.obs_source_get_settings(source)
        obs_display = obs.obs_data_get_int(source_settings, "display")
        self.source_size.x = obs.obs_source_get_width(source)
        self.source_size.y = obs.obs_source_get_height(source)
        obs.obs_source_release(current_scene_as_source)

        # Find the active display settings
        for screen in pwc.getAllScreens().items():
            if screen[1]['id'] == obs_display:
                print(f"Found monitor {screen[0]}")
                self.screen = screen[1]

        if not self.screen:
            print("Failed finding the screen!")

        self.init_hotkeys(settings)

    def init_hotkeys(self, settings):
        def set_follow(pressed):
            if not pressed:
                return

            self.set_mode(ZoomFollowStates.FOLLOW)

        def set_rect(pressed):
            if not pressed:
                return

            pos = pwc.getMousePos()
            if not self.verify_display(pos):
                print('Clicked outside the active display')
                return

            if not self.rect:
                print("First press")
                self.rect = obs.vec4()
                self.rect.x = pos.x
                self.rect.y = pos.y
                print(f"Mouse Pos: {pos.x}, {pos.y}")
            else:
                print("Second press")
                self.rect.z = pos.x
                self.rect.w = pos.y

                print(f"Rect: {self.rect.x}, {self.rect.y}, {self.rect.z}, {self.rect.w}")
                print(f"Bounds: {self.source_size.x}, {self.source_size.y}")
                self.set_mode(ZoomFollowStates.RECT)

                crop = obs.obs_sceneitem_crop()
                crop.left = int(self.rect.x)
                crop.right = int(self.source_size.x) - int(self.rect.z)
                crop.top = int(self.rect.y)
                crop.bottom = int(self.source_size.y) - int(self.rect.w)
                self.set_target_crop(crop)
                
                self.rect = None

        def set_window(pressed):
            if pressed:
                print("Pressed hotkey 3")

        def reset(pressed):
            if not pressed:
                return

            self.set_mode(ZoomFollowStates.NONE)
            self.set_target_crop(obs.obs_sceneitem_crop())

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

    def verify_display(self, pos):
        screen_pos = self.screen['pos']
        screen_size = self.screen['size']
        in_x = (pos.x - screen_pos.x >= 0 and pos.x - screen_pos.x <= screen_size.width)
        in_y = (pos.y + screen_pos.y >= 0 and pos.y + screen_pos.y <= screen_size.height)
        print(f"Mouse: {pos.x - screen_pos.x}, {in_x}, {pos.y + screen_pos.y}, {in_y}")
        return in_x and in_y

    def set_target_crop(self, target_crop):
        self.target_crop = target_crop
        self.crop = target_crop
        obs.obs_sceneitem_set_crop(self.scene_item, self.crop)

    def tick(self, seconds):
        if self.scene_item and self.mode == ZoomFollowStates.FOLLOW:
            pos = pwc.getMousePos()
            if self.verify_display(pos):
                crop = obs.obs_sceneitem_crop()
                crop.left = int(pos.x)
                crop.right = int((self.source_size.x/2) - pos.x)
                crop.top = int(pos.y)
                crop.bottom = int((self.source_size.y/2) - pos.y)
                self.set_target_crop(crop)

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