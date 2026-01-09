from popup_windows.settings_layout import Ui_Settings
import json

class SettingsBackend:
    def __init__(self, settings_ui, main_window):
        self.settings_ui = settings_ui
        self.main_window = main_window
        self.mol_viewer_save_file_num = None
        self.mol_viewer_import_file_num = None

    def connect_signals(self):

        #===General/Appearance===
        self.settings_ui.SettingsAppearanceTabDefaultButton.clicked.connect(self.main_window.default_appearance)
        self.settings_ui.SettingsAppearanceTabFontComboBox.currentIndexChanged.connect(self.main_window.change_font)
        self.settings_ui.SettingsAppearanceTabTextSizeSpinBox.valueChanged.connect(self.main_window.change_font)
        self.settings_ui.SettingsAppearanceTabLoadQSSButton.clicked.connect(self.main_window.load_style_sheet)
        self.settings_ui.SettingsAppearanceTabThemeComboBox.currentIndexChanged.connect(self.main_window.change_theme)
        self.settings_ui.SettingsAppearanceTabRESETALLButton.clicked.connect(self.main_window.RESET_ALL)

        #===Search====
        self.settings_ui.SettingsSearchTabChemSpiKeyLineEdit.editingFinished.connect(self.main_window.searchAndFiles.update_cskey)
        self.settings_ui.SettingsSearchTabDirectoryLineEdit.editingFinished.connect(self.search_change_directory)

        #===Molecule Viewer===
        self.settings_ui.SettingsMolViewerTabSaveFileComboBox.currentIndexChanged.connect(self.mol_viewer_save_file_type)
        self.settings_ui.SettingsMolViewerTabImportFileComboBox.currentIndexChanged.connect(self.mol_viewer_import_file_type)
        self.settings_ui.SettingsMolViewerTabStyleComboBox.currentIndexChanged.connect(self.change_mol_viewer_style)
        self.settings_ui.SettingsMolViewerTabAtomColorsComboBox.currentIndexChanged.connect(self.change_mol_viewer_atom_colors)
#TODO: put the dropdown boxes in the right places
       
    
    #===General/Appearance===
    
    def search_change_directory(self):
        #TODO: add savign logic into toher code backend and make sure it take from here or uses a default
        pass
    

    #===Molecule Viewer===
    def change_mol_viewer_atom_colors(self):
        with open("tab_backends/molecule_viewer_functions/molecule_viewer_settings.json", "r") as file:
            data = json.load(file)
        index = self.settings_ui.SettingsMolViewerTabAtomColorsComboBox.currentIndex()
        colorschemes = ["Jmol", "default", "greenCarbon", "cyanCarbon", "yellowCarbon", "whiteCarbon", "orangeCarbon", "lightGrayCarbon","purpleCarbon", "spectrum"]
        if 0 <= index < len(colorschemes):
            data["colorscheme"] = colorschemes[index]

        with open("tab_backends/molecule_viewer_functions/molecule_viewer_settings.json", "w") as file:
            json.dump(data, file, indent=4)
        self.main_window.moleculeViewerTab.update_display()

    def mol_viewer_save_file_type(self):
        index = self.settings_ui.SettingsMolViewerTabSaveFileComboBox.currentIndex()
        text_options = ["Save As PDB", "Save As Mol", "Save As SDF", "Save As SMILES", "Save As InChI", "Save As TDT", "Save As JSON" "Save As Mrv", "Save As XYZ","Save As TPL", "Save As FASTA", "Save As HELM", "Save As SMARTS", "Save As CML"]
        if 0 <= index < len(text_options):
            self.mol_viewer_save_file_num = index
            text = text_options[index]
            self.main_window.ui.PybraneMolViewerSaveFileButton.setText(text)

    def mol_viewer_import_file_type(self):
        index = self.settings_ui.SettingsMolViewerTabImportFileComboBox.currentIndex()
        text_options = ["Import PDB", "Import Mol", "Import SDF", "Import SMILES", "Import InChI", "Import TDT", "Import Mrv", "Import XYZ","Import TPL", "Import FASTA", "Import HELM", "Import SMARTS", "Import CDXML"]
        if 0 <= index < len(text_options):
            self.mol_viewer_import_file_num = index
            text = text_options[index]
            self.main_window.ui.PybraneMolViewerImportSmilesButton.setText(text)

    def change_mol_viewer_style(self):
        with open("tab_backends/molecule_viewer_functions/molecule_viewer_settings.json", "r+") as file:
            data = json.load(file)
        index = self.settings_ui.SettingsMolViewerTabStyleComboBox.currentIndex()
        styles = ["stick", "line", "cross", "sphere", "cartoon", "tube", "ribbon"]
        if 0 <= index < len(styles):
            data["style"] = styles[index]


        with open("tab_backends/molecule_viewer_functions/molecule_viewer_settings.json", "w") as file:
            json.dump(data, file, indent=4)
        self.main_window.moleculeViewerTab.update_display()
