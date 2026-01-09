class SecondViewer(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.resize(620, 559)

        #=== Layout ===
        self.analysisViewerLayout = QtWidgets.QGridLayout(self)
        self.analysisViewerLayout.setObjectName("analysisViewerLayout")

        #=== OpenGL Display ===
        self.analysisViewerDisplayWidget = genericOpenGLWidget()
        self.analysisViewerDisplayWidget.setObjectName("analysisViewerDisplayWidget")
        self.analysisViewerLayout.addWidget(self.analysisViewerDisplayWidget, 0, 0, 1, 4)

        #=== Row 1 Buttons ===
        self.analysisViewerZoomOutMaxButton = QtWidgets.QPushButton(self)
        self.analysisViewerZoomOutMaxButton.setObjectName("analysisViewerZoomOutMaxButton")
        self.analysisViewerLayout.addWidget(self.analysisViewerZoomOutMaxButton, 1, 0, 1, 1)

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
        self.analysisViewerZoomInMaxButton = QtWidgets.QPushButton(self)
        self.analysisViewerZoomInMaxButton.setObjectName("analysisViewerZoomInMaxButton")
        self.analysisViewerLayout.addWidget(self.analysisViewerZoomInMaxButton, 2, 0, 1, 1)

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
        self.analysisViewerZoomInMaxButton.clicked.connect(window.ana.zoom_in_max)
        self.analysisViewerZoomOutMaxButton.clicked.connect(window.ana.zoom_out_max)
        self.analysisViewerMinimizeButton.clicked.connect(window.ana.minimize_viewer)
        self.analysisViewerAutoRotateButton.clicked.connect(window.ana.auto_rotate)
        self.analysisViewerFullScreenButton.clicked.connect(window.ana.expand_viewer)
        self.analysisViewerChangeStyleButton.clicked.connect(window.ana.change_style)
        self.analysisViewerLoadFileButton.clicked.connect(window.ana.load_file)
        self.analysisViewerSaveFileButton.clicked.connect(window.ana.save_file)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Analytical Viewer"))
        self.analysisViewerZoomOutMaxButton.setText(_translate("Form", "Max Zoom Out"))
        self.analysisViewerLoadFileButton.setText(_translate("Form", "Load File"))
        self.analysisViewerAutoRotateButton.setText(_translate("Form", "Auto Rotate"))
        self.analysisViewerFullScreenButton.setText(_translate("Form", "Full Screen"))
        self.analysisViewerZoomInMaxButton.setText(_translate("Form", "Max Zoom In"))
        self.analysisViewerSaveFileButton.setText(_translate("Form", "Save File"))
        self.analysisViewerChangeStyleButton.setText(_translate("Form", "Change View Style"))
        self.analysisViewerMinimizeButton.setText(_translate("Form", "Minimize"))
