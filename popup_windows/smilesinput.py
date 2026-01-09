from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QVBoxLayout, QDialog, QDialogButtonBox, QMessageBox
from PyQt5 import QtOpenGL
from PyQt5 import QtWidgets
#from OpenGL import GLU
from rdkit.Chem import rdDepictor as rdd
from rdkit.Chem.Draw import rdMolDraw2D as draw2D
from rdkit import Chem

from rdkit.Chem import Draw, AllChem
#from rdkit.Chem.Draw import DrawingOptions
class SMILESInputWindow(QtWidgets.QDialog):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle('SMILES Input Window')
        self.setGeometry(150, 150, 300, 200)

        #=== Layout ===
        self.molecularViewerSMILESInputLayout = QVBoxLayout()

        #=== Input Field ===
        self.molecularViewerSMILESInputField = QLineEdit(self)
        self.molecularViewerSMILESInputLayout.addWidget(self.molecularViewerSMILESInputField)

        #=== OK / Cancel Buttons ===
        self.molecularViewerSMILESDialogButtonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self
        )
        self.molecularViewerSMILESDialogButtonBox.accepted.connect(self.acceptInput)
        self.molecularViewerSMILESDialogButtonBox.rejected.connect(self.reject)
        self.molecularViewerSMILESInputLayout.addWidget(self.molecularViewerSMILESDialogButtonBox)

        self.setLayout(self.molecularViewerSMILESInputLayout)

    def acceptInput(self):
        smiles_input = self.molecularViewerSMILESInputField.text()
        self.molecularViewerSMILESMolInput = Chem.MolFromSmiles(smiles_input)
        self.main_window.moleculeViewerTab.smiles_read()
        self.close()
