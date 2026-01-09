import webbrowser
class HomescreenBackend:
    def __init__(self, main_window):
        self.main_window = main_window

    def open_credits(self):
        webbrowser.open('XXXXX')

    def open_settings(self):
        #todo: create a new main settings window
        pass
    def open_manual(self):
        webbrowser.open('XXXXX')
        
    def load_pybrane(self):
        self.main_window.ui.AppLayoutsHolderStackedWidget.setCurrentIndex(1)
        