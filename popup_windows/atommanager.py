from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QVBoxLayout, QDialog, QDialogButtonBox, QMessageBox
from PyQt5 import QtOpenGL
from PyQt5 import QtWidgets
#from OpenGL import GLU
class MolecularViewerAtomManager(QtWidgets.QDialog):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle('Atom Manager')
        self.setGeometry(150, 150, 300, 200)

        #=== Layout ===
        self.MolecularViewerAtomManagerLayout = QtWidgets.QGridLayout(self)
        self.MolecularViewerAtomManagerLayout.setObjectName("MolecularViewerAtomManagerLayout")

        #=== Atom ID Label and SpinBox ===
        self.MolecularViewerAtomManagerIDLabel = QtWidgets.QLabel(self)
        self.MolecularViewerAtomManagerIDLabel.setObjectName("MolecularViewerAtomManagerIDLabel")
        self.MolecularViewerAtomManagerLayout.addWidget(self.MolecularViewerAtomManagerIDLabel, 0, 0, 1, 1)

        self.MolecularViewerAtomManagerIDSpinBox = QtWidgets.QSpinBox(self)
        self.MolecularViewerAtomManagerIDSpinBox.setObjectName("MolecularViewerAtomManagerIDSpinBox")
        self.MolecularViewerAtomManagerLayout.addWidget(self.MolecularViewerAtomManagerIDSpinBox, 1, 0, 1, 1)

        self.MolecularViewerAtomManagerAddRadioButton = QtWidgets.QRadioButton(self)
        self.MolecularViewerAtomManagerAddRadioButton.setObjectName("MolecularViewerAtomManagerAddRadioButton")
        self.MolecularViewerAtomManagerLayout.addWidget(self.MolecularViewerAtomManagerAddRadioButton, 1, 1, 1, 1)

        #=== Atomic Number Label and SpinBox ===
        self.MolecularViewerAtomManagerAtomicNumberLabel = QtWidgets.QLabel(self)
        self.MolecularViewerAtomManagerAtomicNumberLabel.setObjectName("MolecularViewerAtomManagerAtomicNumberLabel")
        self.MolecularViewerAtomManagerLayout.addWidget(self.MolecularViewerAtomManagerAtomicNumberLabel, 2, 0, 1, 1)

        self.MolecularViewerAtomManagerAtomicNumberSpinBox = QtWidgets.QSpinBox(self)
        self.MolecularViewerAtomManagerAtomicNumberSpinBox.setObjectName("MolecularViewerAtomManagerAtomicNumberSpinBox")
        self.MolecularViewerAtomManagerLayout.addWidget(self.MolecularViewerAtomManagerAtomicNumberSpinBox, 3, 0, 1, 1)

        self.MolecularViewerAtomManagerRemoveRadioButton = QtWidgets.QRadioButton(self)
        self.MolecularViewerAtomManagerRemoveRadioButton.setObjectName("MolecularViewerAtomManagerRemoveRadioButton")
        self.MolecularViewerAtomManagerLayout.addWidget(self.MolecularViewerAtomManagerRemoveRadioButton, 3, 1, 1, 1)

        #=== Dialog Buttons ===
        self.MolecularViewerAtomManagerDialogButtonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.MolecularViewerAtomManagerDialogButtonBox.setObjectName("MolecularViewerAtomManagerDialogButtonBox")
        self.MolecularViewerAtomManagerLayout.addWidget(self.MolecularViewerAtomManagerDialogButtonBox, 5, 0, 1, 1)

        self.MolecularViewerAtomManagerDialogButtonBox.accepted.connect(self.acceptInput)
        self.MolecularViewerAtomManagerDialogButtonBox.rejected.connect(self.reject)

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.MolecularViewerAtomManagerIDLabel.setText(_translate("Dialog", "Atom ID"))
        self.MolecularViewerAtomManagerAddRadioButton.setText(_translate("Dialog", "Add"))
        self.MolecularViewerAtomManagerAtomicNumberLabel.setText(_translate("Dialog", "Atomic Number"))
        self.MolecularViewerAtomManagerRemoveRadioButton.setText(_translate("Dialog", "Remove"))

    def acceptInput(self):
        self.main_window.moleculeViewerTab.manage_atoms()
        self.close()
