import webbrowser
class MenuActions:
    def __init__(self, main_window):
        self.main_window = main_window
   
    def quit_application(self):
        # TODO: find name of the tab widget and p[ut in here plz/add new names in]
        tabNumber = self.main_window.ui.PybraneCenterWidget.currentIndex()
        if tabNumber == 1 or tabNumber == 2:
            self.main_window.ui.PybraneShellDebugTextBox.append("WARNING: Please verify all proccesses have finished and swtich to the analysis or molecule editor tab to close window.")
        else:
            self.main_window.close()

    def open_main_menu(self):
        self.main_window.ui.AppLayoutsHolderStackedWidget.setCurrentIndex(1)

    def open_general_settings(self):
        self.main_window.settingswindow.show()
        self.main_window.settingsdialog.SettingsTabWidget.setCurrentIndex(0)

    def maximize_window(self):
        self.main_window.showMaximized()

    def minimize_window(self):
        self.main_window.showMinimized()

    def show_about_dialog(self):
        # TODO: Implement logic to show the About dialog
        pass

    def open_source_code_page(self):
        webbrowser.open('https://github.com/elusive-e/pybrane')

    def open_faq(self):
        # TODO: Implement logic to open FAQ documentation
        pass

    def open_help_documentation(self):
        # TODO: Implement logic to open help documentation
        pass

    def open_feedback_form(self):
        # TODO: Implement logic to open feedback form or page
        webbrowser.open('https://github.com/elusive-e/pybrane')

    def open_graph_settings(self):
        self.main_window.settingswindow.show()
        self.main_window.settingsdialog.SettingsTabWidget.setCurrentIndex(7)

    def open_key_file_settings(self):
        self.main_window.settingswindow.show()
        self.main_window.settingsdialog.SettingsTabWidget.setCurrentIndex(1)
        

    def open_other_settings(self):
        self.main_window.settingswindow.show()
        self.main_window.settingsdialog.SettingsTabWidget.setCurrentIndex(2)
        