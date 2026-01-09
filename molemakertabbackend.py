class MoleculeMakerTab:
    def __init__(self, MainMainWindow):
        self.MainMainWindow = MainMainWindow
        self.TwoDView = False
        self.MolInput = None

        # === 'File' Column Button Signals ===
        self.PybraneMolViewerSaveFileButton.clicked.connect(self.SaveFile)
        self.PybraneMolViewerImportSmilesButton.clicked.connect(self.BLANK_13)
        self.PybraneMolViewerLoadPDBButon.clicked.connect(self.BLANK_12)

        # === 'Edit' Column Button Signals ===
        self.PybraneMolViewerEditAtomsButton.clicked.connect(self.BLANK_11)
        self.PybraneMolViewerEditBondsButton.clicked.connect(self.BLANK_9)
        self.PybraneMolViewerEditApperanceButton.clicked.connect(self.BLANK_27)

        # === 'Misc' Column Button Signals ===
        self.PybraneMolViewerSwtichDisplayButton.clicked.connect(self.BLANK_10)
        self.PybraneMolViewerSwitchFilesButton.clicked.connect(self.BLANK_27)
        self.PybraneMolViewerExamplesButton.clicked.connect(self.BLANK_27)

        # === RdKit SVG Settings ===
        DrawingOptions.bondLineWidth = 1.2
        DrawingOptions.atomLabelFontSize = 10
        DrawingOptions.includeAtomNumbers = True

    def SaveFile(self):
        # Convert molecule to PDB and write to a default file
        self.MolInput = Chem.Mol(self.MolInput)
        Content = Chem.rdmolfiles.MolToPDBBlock(self.MolInput)
        with open("MoleculeMakerExport.pdb", 'w') as File:
            File.write(Content) 

    def SaveFileAs(self):
        # Prompt user for file path and save PDB content
        MolInput = self.MolInput
        MolInput = Chem.MolToPDBBlock(self.MolInput)
        FileName, _ = QFileDialog.getSaveFileName(self, "Save File", "", "All Files(*);;Text Files(*.txt)", options=options)
        if FileName:
            File = open(FileName, 'w')
            File.write(MolInput)
            self.setWindowTitle(str(os.path.basename(FileName)))
            File.close()
        else:
            window.Text_browser13.append("WARNING: No file name provided, file HAS NOT BEEN SAVED. Please try again.")

    def SwitchDisplay(self, TwoDView):
        # Toggle between 2D and 3D molecular display
        self.TwoDView = not self.TwoDView
        MolInput = self.MolInput
        print(self.MolInput)
        self.UpdateDisplay(MolInput)

    def UpdateDisplay(self, MolInput):
        # Update molecule visualization based on current view mode
        self.MolInput = MolInput

        # === Common drawing settings ===
        DrawingOptions.bondLineWidth = 1.2   
        DrawingOptions.atomLabelFontSize = 10
        DrawingOptions.includeAtomNumbers = True

        if self.TwoDView:
            # === 2D Rendering ===
            print(self.MolInput)
            window.tabWidget.setCurrentIndex(1)
            BackupMol = self.MolInput
            print(BackupMol)

            if self.MolInput.GetNumConformers() == 0:
                AllChem.Compute2DCoords(self.MolInput)

            Drawer = Draw.rdMolDraw2D.MolDraw2DSVG(300, 300)
            Draw.rdMolDraw2D.PrepareAndDrawMolecule(Drawer, self.MolInput)
            Drawer.FinishDrawing()
            Svg = Drawer.GetDrawingText()

            with open('initial_mol.svg', 'w') as File:
                File.write(Svg)

            window.graphicsView.load('initial_mol.svg')
            self.MolInput = BackupMol
        else:
            # === 3D Rendering ===
            print(self.MolInput)
            try:
                window.tabWidget.setCurrentIndex(0)
                if self.MolInput.GetNumConformers() == 0:
                    self.MolInput = Chem.Mol(self.MolInput)
                    self.MolInput = AllChem.AddHs(self.MolInput, addCoords=True)
                    AllChem.EmbedMolecule(self.MolInput, AllChem.ETKDG())
                    AllChem.MMFFOptimizeMolecule(self.MolInput)

                MolInput = Chem.AddHs(self.MolInput)
                AllChem.EmbedMolecule(self.MolInput)

                Conformer = self.MolInput.GetConformer()
                AtomPositions = []

                for Atom in self.MolInput.GetAtoms():
                    Pos = Conformer.GetAtomPosition(Atom.GetIdx())
                    AtomPositions.append({
                        'element': Atom.GetSymbol(),
                        'radius': Chem.GetPeriodicTable().GetRvdw(Atom.GetAtomicNum()),
                        'position': np.array([Pos.x, Pos.y, Pos.z])
                    })

                self.AtomPositions = AtomPositions
                window.openGLWidget.setFocus()
                window.openGLWidget.raise_()
                window.openGLWidget.set_coordinates(AtomPositions)
            except:
                window.textBrowser_18.append("ERROR: Your molecule could not be visualized. Please make sure there are no errors in the file.")

    def LoadPDBMMMM(self, MolInput):
        # Load molecule from selected PDB file
        FilePath, _ = QtWidgets.QFileDialog.getOpenFileName(window, "Open File", "", "All Files (*)")
        if FilePath:
            with open(FilePath, 'r') as File:
                Content = File.read()
            MolInput = Chem.MolFromPDBBlock(Content)
            window.molecule_maker_tab.UpdateDisplay(self, MolInput)
        else:
            window.textBrowser_13.append("WARNING: The file chosen is not the correct format or has not been picked.")

    def SmilesImport(self):
        # Show SMILES input dialog
        smilesdialog.show()

    def SmilesRead(self):
        # Convert SMILES string to molecule and update display
        SmilesInput = smilesdialog.inputField.text().strip()
        MolInput = Chem.MolFromSmiles(SmilesInput)
        window.mmmm.UpdateDisplay(MolInput)

    def StartAtoms(self):
        # Launch atom editing dialog
        atomdialog.show()

    def StartBonds(self):
        # Launch bond editing dialog
        bonddialog.show()

    def ManageBonds(self):
        # Manage bond addition/removal between atoms
        Atom1 = bonddialog.spinBox.value()
        Atom2 = bonddialog.spinBox_2.value()
        AddBond = bonddialog.radioButton.isChecked()
        RemoveBond = bonddialog.radioButton_2.isChecked()
        BondChoice = bonddialog.comboBox.choice()
        RWUserMol = Chem.RWMol(self.MolInput)

        try:
            if AddBond and RemoveBond:
                window.textBox_18.append("WARNING: You must pick one bond action, not both.")
            if AddBond:
                RWUserMol.AddBond(Atom1, Atom2, order=Chem.rdchem.BondType.BondChoice)
            if RemoveBond:
                RWUserMol.RemoveBond(Atom1, Atom2, order=Chem.rdchem.BondType.BondChoice)
            else:
                window.textBox_18.append("WARNING: You must pick one bond action, not none")
            self.MolInput = RWUserMol
            self.UpdateDisplay()
        except:
            window.textBrowser_18.append("ERROR: The bond picked could not be updated.")

    def ManageAtoms(self):
        # Manage atom addition/removal
        Atom1 = atomdialog.spinBox.value()
        AddAtom = atomdialog.radioButton.isChecked()
        RemoveAtom = atomdialog.radioButton_2.isChecked()
        MolInput = window.mmmm.MolInput
        RWUserMol = Chem.RWMol(MolInput)
        UserAtomIndex = atomdialog.spinBox.value()

        try:
            if AddAtom and RemoveAtom:
                window.textBrowser_18.append("WARNING: You must pick one atom action, not both.")
            if AddAtom:
                NewAtom = Chem.Atom(UserAtomIndex)
                RWUserMol.AddAtom(UserAtomIndex)
                window.textBrowser_18.append(f"Atom added at index: {RWUserMol.GetNumAtoms() - 1}")
            if RemoveAtom:
                RWUserMol.RemoveAtom(UserAtomIndex)
                window.textBrowser_18.append(f"Atom removed at index: {UserAtomIndex}")
            else:
                window.textBrowser_18.append("WARNING: You must pick one atom action, not none")
            self.MolInput = RWUserMol
            window.mmmm.UpdateDisplay(RWUserMol)
        except Exception as Error:
            window.textBrowser_18.append(f"Error: {str(Error)}")
