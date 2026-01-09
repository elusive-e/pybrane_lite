from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QVBoxLayout, QDialog, QDialogButtonBox, QMessageBox
from PyQt5 import QtOpenGL
from PyQt5 import QtWidgets
#from OpenGL import GLU
class CSInputWindow(QtWidgets.QDialog):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle('Chemistry Spider Input Window')
        self.setGeometry(150, 150, 300, 200)

        self.layout = QVBoxLayout()

        self.inputField = QLineEdit(self)
        self.layout.addWidget(self.inputField)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.buttonBox.accepted.connect(self.acceptInput)
        self.buttonBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonBox)

        self.setLayout(self.layout)

    def acceptInput(self):
        self.main_window.searchAndFiles.update_cskey()
        self.close()