from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QVBoxLayout, QDialog, QDialogButtonBox, QMessageBox
from PyQt5 import QtOpenGL
from PyQt5 import QtWidgets
#from OpenGL import GLU
#from openmm.app import appv
from openmm import *
from openmm.unit import *
from openmm.app import *
from openmm import *
#from pdbfixer import PDBFixer
from openmm.unit import *
from sys import stdout
import pandas as pd
import MDAnalysis
import numpy as np
import random
from chatterbot import ChatBot
import sys
import re
import subprocess
#Simport pdbfixer
print("importing stuff")
import requests
#import yaml
from popup_windows.smilesinput import SMILESInputWindow
from popup_windows.atommanager import MolecularViewerAtomManager
from popup_windows.bondmanager import MolecularViewerBondManager
from popup_windows.extraviewer import SecondViewer
from popup_windows.cskeyinput import CSInputWindow

from tab_backends.filesprebeta import SearchAndFiles
from tab_backends.molemakertabbackend import MoleculeViewerTab
from tab_backends.menufunctions import MenuActions
from tab_backends.homescreen_backend import HomescreenBackend

#from tab_backends.molecule_viewer_functions.opengl_generic import genericOpenGLWidget
from meme import Ui_MainWindow
from tab_backends.lesson_backend import LessonBackend

from popup_backend.settingsbackend import SettingsBackend
from popup_windows.settings_layout import Ui_Settings
#import openai
import webbrowser
print("importing stuff4")
#from bs4 import BeautifulSoup

# from chatterbot import ChatBot
# from chatterbot.trainers import ListTrainer
# from chatterbot.trainers import ChatterBotCorpusTrainer
import sys
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import random
from PyQt5.QtGui import QFont

from rdkit.Chem import rdDepictor as rdd
from rdkit.Chem.Draw import rdMolDraw2D as draw2D
from rdkit import Chem
#Sfrom rdkit.Chem.Draw import DrawingOptions
from rdkit.Chem import Draw, AllChem
import wikipedia 
from chemspipy import ChemSpider
import matplotlib
michael = ChatBot("Michael")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
#michael = ChatBot("Michael")
matplotlib.use('Qt5Agg')
import mdtraj as md
from meme import Ui_MainWindow
print("importing stuff8")
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)      
        self.initialize_backend()
        self.initialize_extra_windows()
        self.menu_connect_signals()
        self.buttons_connect_signals()
        self.set_defaults()
        # Initialize tab handlers, pass self so they can access UI and dialogs
        #instances are inCamelCase and the actual class IsInPascalCase
    def initialize_backend(self):
        print("intiilaize")
        self.moleculeViewerTab = MoleculeViewerTab(self)
        
        self.searchAndFiles = SearchAndFiles(self)
        self.menuActions = MenuActions(self)
        self.homescreenActions = HomescreenBackend(self)
        self.lessonBackend = LessonBackend(main_window=self)

    def initialize_extra_windows(self):
        # Initialize dialogs here with parenting
        #TO DO: seperate all extra windows like the settings
        self.smilesdialog = SMILESInputWindow(main_window=self)
        self.bonddialog = MolecularViewerBondManager(main_window=self)
        self.atomdialog = MolecularViewerAtomManager(main_window=self)
        self.viewerwindow = SecondViewer(main_window=self)
        self.settingsdialog = Ui_Settings()
        self.settingswindow = QtWidgets.QDialog()
        self.settingsdialog.setupUi(self.settingswindow)
        self.settingsBackend = SettingsBackend(self.settingsdialog, self)
        self.settingsBackend.connect_signals()
        print("initiliaizng stuff")
        # Hide dialogs initially
        self.smilesdialog.hide()
        self.bonddialog.hide()
        self.atomdialog.hide()
        self.settingswindow.hide()
        self.viewerwindow.hide()
        
    def menu_connect_signals(self):
        print("signals stuff")
        # === 'File' Menu Actions ===
        self.ui.actionQuit.triggered.connect(self.menuActions.quit_application)
    
        self.ui.actionMain_Menu.triggered.connect(self.menuActions.open_main_menu)

        # === 'Settings' Menu Actions ===
        self.ui.actionPyBRANE_General_Settings.triggered.connect(self.menuActions.open_general_settings)
#         self.ui.actionPyBRANE_Graph_Settings.triggered.connect(self.menuActions.open_graph_settings)
#         self.ui.actionPyBRANE_Key_and_File_Settings.triggered.connect(self.menuActions.open_key_file_settings)
        self.ui.actionOther_Settings.triggered.connect(self.menuActions.open_other_settings)

        # === 'Window' Menu Actions ===
        self.ui.actionMaximize.triggered.connect(self.menuActions.maximize_window)
        self.ui.actionMinimize.triggered.connect(self.menuActions.minimize_window)

        # === 'Help' Menu Actions ===
        self.ui.actionAboutPyBRANE.triggered.connect(self.menuActions.show_about_dialog)
        self.ui.actionSource_Code.triggered.connect(self.menuActions.open_source_code_page)
        self.ui.actionFAQ.triggered.connect(self.menuActions.open_faq)
        self.ui.actionHelp.triggered.connect(self.menuActions.open_help_documentation)
        self.ui.actionFeedback.triggered.connect(self.menuActions.open_feedback_form)


    def buttons_connect_signals(self):
        #=== Main Menu Buttons ===
        self.ui.HomescreenCreditsButton.clicked.connect(self.homescreenActions.open_credits)
        self.ui.HomescreenSettingsButton.clicked.connect(self.homescreenActions.open_settings)
        self.ui.HomescreenOpenManualButton.clicked.connect(self.homescreenActions.open_manual)
        self.ui.HomescreenLoadPybraneButton.clicked.connect(self.homescreenActions.load_pybrane)
        
        #=== File Tab Buttons ===
        self.ui.PybranePDBSearchButton.clicked.connect(self.searchAndFiles.search_pdb)
        self.ui.PybraneWikipediaSearchButton.clicked.connect(self.searchAndFiles.search_wiki)
        self.ui.PybraneChemSpiSearchButton.clicked.connect(self.searchAndFiles.search_chemspi)        
        self.ui.PybraneMemBankSearchButton.clicked.connect(self.searchAndFiles.search_lipid_maps)

        #=== 'File' Molecule Viewer Buttons ===
        self.ui.PybraneMolViewerImportSmilesButton.clicked.connect(self.moleculeViewerTab.smiles_import)
        self.ui.PybraneMolViewerLoadPDBButon.clicked.connect(self.moleculeViewerTab.load_pdb)
        self.ui.PybraneMolViewerSaveFileButton.clicked.connect(self.moleculeViewerTab.save_file_as)

        #=== 'Edit' Molecule Viewer Buttons ===
        self.ui.PybraneMolViewerEditAtomsButton.clicked.connect(self.moleculeViewerTab.start_atoms)
        self.ui.PybraneMolViewerEditBondsButton.clicked.connect(self.moleculeViewerTab.start_bonds)
        self.ui.PybraneMolViewerEditApperanceButton.clicked.connect(self.moleculeViewerTab.manage_appearance)

        #=== 'Misc' Molecule Viewer Buttons ===
        self.ui.PybraneMolViewerSwitchDisplayButton.clicked.connect(self.moleculeViewerTab.switch_display)
        self.ui.PybraneMolViewerSwitchFilesButton.clicked.connect(self.moleculeViewerTab.file_settings)
        self.ui.PybraneMolViewerExamplesButton.clicked.connect(self.moleculeViewerTab.load_examples)        #=== Michael and Command Line Buttons ===
        self.ui.PybraneMichaelEnterButton.clicked.connect(self.use_michael)
        self.ui.PybraneShellEnterButton.clicked.connect(self.execute_command)

        #=== Lesson Selection ===
#         self.ui.PybraneLessonTabLessonComboBox.valueChanged.connect(self.lessonBackend.lesson_changed)
#         self.ui.PybraneLessonTabUnitComboBox.valueChanged.connect(self.lessonBackend.unit_changed)
# #         self.ui.PybraneLessonTabLevelComboBox.valueChanged.connect(self.lessonBackend.level_changed)
    def set_defaults(self):
        
        if self.settingsBackend.mol_viewer_import_file_num == None:
            self.settingsBackend.mol_viewer_import_file_num = 0
        if self.settingsBackend.mol_viewer_save_file_num == None:
            self.settingsBackend.mol_viewer_save_file_num =0
        else:
            pass
        
    def execute_command(self):
        command = self.ui.PybraneShellLineEdit.text().strip()
        if command:
            self.ui.PybraneShellDebugTextBox.append(f'> {command}')
            self.ui.PybraneShellLineEdit.clear()
            
            try:
                result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
                output = result.stdout if result.stdout else result.stderr
            except subprocess.TimeoutExpired:
                output = 'Command timed out.'
            except Exception as e:
                output = f'Error: {e}'
            
            self.ui.PybraneShellDebugTextBox.append(output)
            
    def use_michael(self):
        query = self.ui.PybraneMichaelUserInputLineEdit.text().strip()
        self.ui.PybraneMichaelResponseTextBox.append(f'You: {query}')
        self.ui.PybraneMichaelUserInputLineEdit.clear()
        exit_conditions = (":q","quit","exit")
        if query in exit_conditions:
            self.ui.PybraneMichaelResponseTextBox.append("Michael: Goodbye! I hope I was able to help you today.")
        if query == '':
            self.ui.PybraneMichaelResponseTextBox.append("Michael: Your response cannot be blank.")
        else:
            try:
                self.ui.PybraneMichaelResponseTextBox.append(f"Michael: {michael.get_response(query)}")
            except Exception as e:
                self.main_window.ui.PybraneShellDebugTextBox.append(
                    f"ERROR:{str(e)}"
                )
                
    def change_font(self):
        font = str(self.settingsBackend.settings_ui.SettingsAppearanceTabFontComboBox.currentFont())
        size = self.settingsBackend.settings_ui.SettingsAppearanceTabTextSizeSpinBox.value()
        app.setFont(QFont(font, size))

    def default_appearance(self):
        with open("ui_and_style/default.qss", "r") as f:
            app.setStyleSheet(f.read())
        font = "Verdana"
        size = "14"
        app.setFont(QFont(font, size))

    def RESET_ALL(self):
        #TODO: Clear all settings to default
        with open("ui_and_style/default.qss", "r") as f:
            app.setStyleSheet(f.read())
        font = "Verdana"
        size = "14"
        app.setFont(QFont(font, size))
        


    def change_theme(self):
        index = self.settingsBackend.settings_ui.SettingsAppearanceTabThemeComboBox.currentIndex()
        style_options = ["ui_and_style/default.qss", "ui_and_style/default_dark.qss", "ui_and_style/sci_fi_dark.qss", "ui_and_style/cherry_blossom_light.qss", 
                         "ui_and_style/neon_dark.qss", "ui_and_style/deep_ocean_dark.qss", "ui_and_style/sand_storm_dark.qss", "ui_and_style/desert_oasis_light.qss", "ui_and_style/coral_reef_light.qss"]
        if 0 <= index < len(style_options):
            with open(style_options[index], "r") as f:
                app.setStyleSheet(f.read())

    def load_style_sheet(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.main_window,
            "Open File",
            "",
            "All Files (*)"
        )
        if file_path:
            with open(file_path, "r") as f:
                app.setStyleSheet(f.read())
        else:
            pass
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    print("window made")
    window = MainWindow()
    window.show()
    print("window openend")
    with open("ui_and_style/default.qss", "r") as f:
        app.setStyleSheet(f.read())
    print("style sheet read")
    sys.exit(app.exec_())
    print("app running")