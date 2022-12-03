import obspython as obs 

"""
Holds all the hotkeys defined for this script
"""
class Hotkey:
    def __init__(self, callback, obs_settings, _id, _description):
        self.obs_data = obs_settings
        self.hotkey_id = obs.OBS_INVALID_HOTKEY_ID
        self.hotkey_saved_key = None
        self.callback = callback
        self._id = _id
        self._description = _description

        self.load_hotkey()
        self.register_hotkey()
        self.save_hotkey()

    def register_hotkey(self):
        print("Register hotkey")

        self.hotkey_id = obs.obs_hotkey_register_frontend(
            "htk_id_" + str(self._id), self._description, self.callback
        )
        obs.obs_hotkey_load(self.hotkey_id, self.hotkey_saved_key)

    def unregister_hotkey(self):
        obs.obs_hotkey_unregister(self.hotkey_id)

    def load_hotkey(self):
        print("Load hotkey")
        self.hotkey_saved_key = obs.obs_data_get_array(
            self.obs_data, "htk_id_" + str(self._id)
        )
        obs.obs_data_array_release(self.hotkey_saved_key)

    def save_hotkey(self):
        print("Save hotkey")

        self.hotkey_saved_key = obs.obs_hotkey_save(self.hotkey_id)
        obs.obs_data_set_array(
            self.obs_data, "htk_id_" + str(self._id), self.hotkey_saved_key
        )
        obs.obs_data_array_release(self.hotkey_saved_key)
