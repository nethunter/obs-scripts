import obspython as obs
from utils.hotkey import Hotkey

class Test:
    hotkeys = []

    def init_hotkeys(self, settings):
        def cb1(pressed):
            if pressed:
                print("Pressed hotkey 1")

        def cb2(pressed):
            if pressed:
                print("Pressed hotkey 2")

        def cb3(pressed):
            if pressed:
                print("Pressed hotkey 3")

        self.hotkeys = [
            Hotkey(cb1, settings, "test1", "Test hotkey 1"),
            Hotkey(cb2, settings, "test2", "Test hotkey 2"),
            Hotkey(cb3, settings, "test3", "Test hotkey 3")
        ]

    def save_hotkeys(self):
        for htk in self.hotkeys:
            htk.save_hotkey()


test = Test()


def script_description():
    return "Hotkey test script"

def script_load(settings):
    test.init_hotkeys(settings)

def script_save(settings):
    test.save_hotkeys()