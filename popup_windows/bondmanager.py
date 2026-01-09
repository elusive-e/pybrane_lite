from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QVBoxLayout, QDialog, QDialogButtonBox, QMessageBox
from PyQt5 import QtOpenGL
from PyQt5 import QtWidgets
#from OpenGL import GLU
class MolecularViewerBondManager(QtWidgets.QDialog):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle('SMILES Input Window')
        self.setGeometry(150, 150, 300, 200)

        #=== Layout ===
        self.MolecularViewerBondManagerLayout = QtWidgets.QGridLayout(self)
        self.MolecularViewerBondManagerLayout.setObjectName("MolecularViewerBondManagerLayout")

        #=== Atom ID Labels ===
        self.MolecularViewerBondManagerAtom1Label = QtWidgets.QLabel(self)
        self.MolecularViewerBondManagerAtom1Label.setObjectName("MolecularViewerBondManagerAtom1Label")
        self.MolecularViewerBondManagerLayout.addWidget(self.MolecularViewerBondManagerAtom1Label, 0, 0, 1, 1)

        self.MolecularViewerBondManagerAtom2Label = QtWidgets.QLabel(self)
        self.MolecularViewerBondManagerAtom2Label.setObjectName("MolecularViewerBondManagerAtom2Label")
        self.MolecularViewerBondManagerLayout.addWidget(self.MolecularViewerBondManagerAtom2Label, 0, 1, 1, 1)

        #=== Atom ID Inputs ===
        self.MolecularViewerBondManagerAtom1SpinBox = QtWidgets.QSpinBox(self)
        self.MolecularViewerBondManagerAtom1SpinBox.setObjectName("MolecularViewerBondManagerAtom1SpinBox")
        self.MolecularViewerBondManagerLayout.addWidget(self.MolecularViewerBondManagerAtom1SpinBox, 1, 0, 1, 1)

        self.MolecularViewerBondManagerAtom2SpinBox = QtWidgets.QSpinBox(self)
        self.MolecularViewerBondManagerAtom2SpinBox.setObjectName("MolecularViewerBondManagerAtom2SpinBox")
        self.MolecularViewerBondManagerLayout.addWidget(self.MolecularViewerBondManagerAtom2SpinBox, 1, 1, 1, 1)

        #=== Bond Type Label ===
        self.MolecularViewerBondManagerTypeLabel = QtWidgets.QLabel(self)
        self.MolecularViewerBondManagerTypeLabel.setObjectName("MolecularViewerBondManagerTypeLabel")
        self.MolecularViewerBondManagerLayout.addWidget(self.MolecularViewerBondManagerTypeLabel, 2, 0, 1, 1)

        #=== Add Bond Option ===
        self.MolecularViewerBondManagerAddRadioButton = QtWidgets.QRadioButton(self)
        self.MolecularViewerBondManagerAddRadioButton.setObjectName("MolecularViewerBondManagerAddRadioButton")
        self.MolecularViewerBondManagerLayout.addWidget(self.MolecularViewerBondManagerAddRadioButton, 2, 1, 2, 1)

        #=== Bond Type ComboBox ===
        self.MolecularViewerBondManagerTypeComboBox = QtWidgets.QComboBox(self)
        self.MolecularViewerBondManagerTypeComboBox.setObjectName("MolecularViewerBondManagerTypeComboBox")
        self.MolecularViewerBondManagerLayout.addWidget(self.MolecularViewerBondManagerTypeComboBox, 3, 0, 1, 1)

        #=== Remove Bond Option ===
        self.MolecularViewerBondManagerRemoveRadioButton = QtWidgets.QRadioButton(self)
        self.MolecularViewerBondManagerRemoveRadioButton.setObjectName("MolecularViewerBondManagerRemoveRadioButton")
        self.MolecularViewerBondManagerLayout.addWidget(self.MolecularViewerBondManagerRemoveRadioButton, 4, 1, 1, 1)

        #=== Dialog Button Box ===
        self.MolecularViewerBondManagerDialogButtonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.MolecularViewerBondManagerDialogButtonBox.setObjectName("MolecularViewerBondManagerDialogButtonBox")
        self.MolecularViewerBondManagerLayout.addWidget(self.MolecularViewerBondManagerDialogButtonBox, 5, 0, 1, 1)

        self.MolecularViewerBondManagerDialogButtonBox.accepted.connect(self.acceptInput)
        self.MolecularViewerBondManagerDialogButtonBox.rejected.connect(self.reject)

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog1", "Bond Manager"))
        self.MolecularViewerBondManagerAtom1Label.setText(_translate("Dialog1", "Atom #1 Id Number"))
        self.MolecularViewerBondManagerAtom2Label.setText(_translate("Dialog1", "Atom #2 Id Number"))
        self.MolecularViewerBondManagerTypeLabel.setText(_translate("Dialog1", "Bond type"))
        self.MolecularViewerBondManagerAddRadioButton.setText(_translate("Dialog1", "Add Bond"))
        self.MolecularViewerBondManagerRemoveRadioButton.setText(_translate("Dialog1", "Remove Bond"))

    def acceptInput(self):
        self.main_window.moleculeViewerTab.manage_bonds()
        self.close()
