from popup_windows.settings_layout import Ui_Settings
import json

class LessonBackend:
    def __init__(self, main_window):
        self.main_window = main_window
        self.mol_viewer_save_file_num = None
        self.mol_viewer_import_file_num = None
        self.analysis_save_file_num = None
        self.analysis_import_file_num = None

    def unit_changed(self):
        pass
    def lesson_changed(self):
        pass
    def level_changed(self):
        pass