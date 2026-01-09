from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QVBoxLayout, QDialog, QDialogButtonBox, QMessageBox
from PyQt5 import QtOpenGL
from PyQt5 import QtWidgets
#from OpenGL import GLU

from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView


import os
html_path = os.path.abspath("tab_backends/molecule_viewer_functions/viewer.html")
class SecondViewer(QtWidgets.QWidget):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.setupUi()

    def setupUi(self):
        self.resize(620, 559)

        #=== Layout ===
        self.analysisViewerLayout = QtWidgets.QGridLayout(self)
        self.analysisViewerLayout.setObjectName("analysisViewerLayout")

        #=== OpenGL Display ===
        self.analysisViewerDisplayWidget = QWebEngineView()
        self.analysisViewerDisplayWidget.load(QUrl.fromLocalFile(html_path))
        self.analysisViewerDisplayWidget.setObjectName("analysisViewerDisplayWidget")
        self.analysisViewerLayout.addWidget(self.analysisViewerDisplayWidget, 0, 0, 1, 4)

        #=== Row 1 Buttons ===
        #add the change atom colors button
        self.analysisViewerAtomColorsButton = QtWidgets.QPushButton(self)
        self.analysisViewerAtomColorsButton.setObjectName("analysisViewerAtomColorsButton")
        self.analysisViewerLayout.addWidget(self.analysisViewerAtomColorsButton, 1, 0, 1, 1)

        self.analysisViewerLoadFileButton = QtWidgets.QPushButton(self)
        self.analysisViewerLoadFileButton.setObjectName("analysisViewerLoadFileButton")
        self.analysisViewerLayout.addWidget(self.analysisViewerLoadFileButton, 1, 1, 1, 1)

        self.analysisViewerAutoRotateButton = QtWidgets.QPushButton(self)
        self.analysisViewerAutoRotateButton.setObjectName("analysisViewerAutoRotateButton")
        self.analysisViewerLayout.addWidget(self.analysisViewerAutoRotateButton, 1, 2, 1, 1)

        self.analysisViewerFullScreenButton = QtWidgets.QPushButton(self)
        self.analysisViewerFullScreenButton.setObjectName("analysisViewerFullScreenButton")
        self.analysisViewerLayout.addWidget(self.analysisViewerFullScreenButton, 1, 3, 1, 1)

        #=== Row 2 Buttons ===
        self.analysisViewerOpenSettingsButton = QtWidgets.QPushButton(self)
        self.analysisViewerOpenSettingsButton.setObjectName("analysisViewerOpenSettingsButton")
        self.analysisViewerLayout.addWidget(self.analysisViewerOpenSettingsButton, 2, 0, 1, 1)

        self.analysisViewerSaveFileButton = QtWidgets.QPushButton(self)
        self.analysisViewerSaveFileButton.setObjectName("analysisViewerSaveFileButton")
        self.analysisViewerLayout.addWidget(self.analysisViewerSaveFileButton, 2, 1, 1, 1)

        self.analysisViewerChangeStyleButton = QtWidgets.QPushButton(self)
        self.analysisViewerChangeStyleButton.setObjectName("analysisViewerChangeStyleButton")
        self.analysisViewerLayout.addWidget(self.analysisViewerChangeStyleButton, 2, 2, 1, 1)

        self.analysisViewerMinimizeButton = QtWidgets.QPushButton(self)
        self.analysisViewerMinimizeButton.setObjectName("analysisViewerMinimizeButton")
        self.analysisViewerLayout.addWidget(self.analysisViewerMinimizeButton, 2, 3, 1, 1)

        self.retranslateUi()

        #=== Connect Buttons to Functions ===
        # self.analysisViewerAtomColorsButton.clicked.connect(self.main_window.analysisTab.zoom_in)
        # self.analysisViewerOpenSettingsButton.clicked.connect(self.main_window.analysisTab.zoom_out)
        # self.analysisViewerMinimizeButton.clicked.connect(self.main_window.analysisTab.minimize_viewer)
        # self.analysisViewerAutoRotateButton.clicked.connect(self.main_window.analysisTab.auto_rotate)
        # self.analysisViewerFullScreenButton.clicked.connect(self.main_window.analysisTab.maximize_viewer)
        # self.analysisViewerChangeStyleButton.clicked.connect(self.main_window.analysisTab.change_style)
        # self.analysisViewerLoadFileButton.clicked.connect(self.main_window.analysisTab.load_molecule_file)
        # self.analysisViewerSaveFileButton.clicked.connect(self.main_window.analysisTab.save_molecule_file)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Analytical Viewer"))
        self.analysisViewerAtomColorsButton.setText(_translate("Form", "Change Colorscheme"))
        self.analysisViewerLoadFileButton.setText(_translate("Form", "Load File"))
        self.analysisViewerAutoRotateButton.setText(_translate("Form", "Auto Rotate"))
        self.analysisViewerFullScreenButton.setText(_translate("Form", "Full Screen"))
        self.analysisViewerOpenSettingsButton.setText(_translate("Form", "Open Settings"))
        self.analysisViewerSaveFileButton.setText(_translate("Form", "Save File"))
        self.analysisViewerChangeStyleButton.setText(_translate("Form", "Change View Style"))
        self.analysisViewerMinimizeButton.setText(_translate("Form", "Minimize"))
