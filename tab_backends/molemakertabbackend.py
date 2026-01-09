from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QVBoxLayout, QDialog, QDialogButtonBox, QMessageBox, QFileDialog
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
from io import StringIO
import numpy as np
import random
import sys
import re
import subprocess
#import pdbfixer
import requests
import json
from rdkit.Chem import rdDepictor as rdd
from rdkit.Chem.Draw import rdMolDraw2D as draw2D
from rdkit import Chem
#from rdkit.Chem.Draw import DrawingOptions
from rdkit.Chem import Draw, AllChem
from rdkit.Chem import inchi
import webbrowser
class MoleculeViewerTab:

    def __init__(self, main_window):
        self.main_window = main_window
        self.two_d_view = False

        # === RdKit SVG Settings ===
#         DrawingOptions.bondLineWidth = 1.2
#         DrawingOptions.atomLabelFontSize = 10
#         DrawingOptions.includeAtomNumbers = True

    def save_file_as(self):
        try: 
            with open("tab_backends/molecule_viewer_functions/molecule.pdb", "r") as file:
                pdb_data = file.read()
            input = Chem.MolFromPDBBlock(pdb_data)
            if self.main_window.settingswindow.mol_viewer_save_file_num == 0:
                data = Chem.MolToPDBBlock(input)

            if self.main_window.settingswindow.mol_viewer_save_file_num == 1:
                data = Chem.MolToMolFile(input)

            if self.main_window.settingswindow.mol_viewer_save_file_num == 2:
                output = StringIO()
                writer = Chem.SDWriter(output)
                writer.write(input)
                writer.close()
                data = output.getvalue()

            if self.main_window.settingswindow.mol_viewer_save_file_num == 3:
                data = Chem.MolToInchi(input)

            if self.main_window.settingswindow.mol_viewer_save_file_num == 4:
                data = Chem.MolToSmiles(input)
                
            if self.main_window.settingswindow.mol_viewer_save_file_num == 5:
                output = StringIO()
                writer = Chem.TDTWriter(output)
                writer.write(input)
                writer.close()
                data = output.getvalue()

            else: 
                data = Chem.MolToPDBBlock(input)
                
            file_name, _ = QFileDialog.getSaveFileName(
                self,
                "Save File",
                "",
                "All Files(*);;Text Files(*.txt)",
                options=options # type: ignore
            )
            if file_name:
                file = open(file_name, 'w')
                file.write(data)
                self.setWindowTitle(str(os.path.basename(file_name)))
                file.close()
            else:
                self.main_window.ui.PybraneShellDebugTextBox.append(
                    "WARNING: No file name provided, file HAS NOT BEEN SAVED. Please try again."
                )
        except Exception as e:
            self.main_window.ui.PybraneShellDebugTextBox.append(
                    f"ERROR:{str(e)}"
                )

    def switch_display(self, two_d_view):
        self.two_d_view = not self.two_d_view
        self.update_display()

    def update_display(self):
        try:
            if self.two_d_view:
                self.main_window.ui.PybraneMolViewerViewHolderWidget.setCurrentIndex(1)
                self.update_2d_display()
            else:
                
                try:
                    self.main_window.ui.PybraneMolViewerViewHolderWidget.setCurrentIndex(0)
                    self.update_3d_display()       
                except Exception:
                    self.main_window.ui.PybraneShellDebugTextBox.append(
                        "ERROR: Your molecule could not be visualized. Please make sure there are no errors in the file."
                    )
        except Exception as e:
            self.main_window.ui.PybraneShellDebugTextBox.append(
                    f"ERROR:{str(e)}"
                )

    def update_2d_display(self):
        try: 
            with open("tab_backends/molecule_viewer_functions/molecule.pdb", "r") as file:
                pdb_data = file.read()
            data = Chem.MolFromPDBBlock(pdb_data)

            width = self.main_window.ui.PybraneMolViewer2DViewScreen.viewport().width()
            height = self.main_window.ui.PybraneMolViewer2DViewScreen.viewport().height()

            drawer = Draw.rdMolDraw2D.MolDraw2DCairo(width, height)
            prepped_data = Draw.rdMolDraw2D.PrepareMolForDrawing(data)
            drawer.DrawMolecule(prepped_data)
            drawer.FinishDrawing()
            png_data = drawer.GetDrawingText()
            image = QtGui.QImage.fromData(png_data)
            pixmap = QtGui.QPixmap.fromImage(image)
            
            scene = self.main_window.ui.PybraneMolViewer2DViewScreen.scene()
            if scene is None:
                scene = QtWidgets.QGraphicsScene()
                self.main_window.ui.PybraneMolViewer2DViewScreen.setScene(scene)
            else:
                scene.clear()

            scene.addPixmap(pixmap)
        except Exception as e:
            sself.main_window.ui.PybraneShellDebugTextBox.append(
                    f"ERROR:{str(e)}"
                )

    def update_3d_display(self):
        try:
            with open("tab_backends/molecule_viewer_functions/molecule_viewer_settings.json", "r") as file:
                settings = json.load(file)
            with open("tab_backends/molecule_viewer_functions/molecule.pdb", "r") as file:
                pdb_data = file.read()
            pdb_data_safe = pdb_data.replace("\n", "\\n")
            js_code = f"""
                        element.removeAllModels();
                       element.addModel(`{pdb_data_safe}`, "pdb");
                       var config = {json.dumps(settings)};
    console.log('PDB Data:', `{pdb_data_safe}`);

                            console.log('Injected config:', config);

                            var styleObj = {{ [config.style]: {{ colorscheme: config.colorscheme }} }};
                            element.setStyle({{}}, styleObj);
                            element.zoomTo();
                            element.render();

                                                                                                                
                        """
            self.main_window.ui.PybraneMolViewer3DViewJSViewer.page().runJavaScript(js_code)
        except Exception as e:
            self.main_window.ui.PybraneShellDebugTextBox.append(
                    f"ERROR:{str(e)}"
                )
    def load_pdb(self):
        try: 
            print("[DEBUG] load_pdb() called.")

            file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
        None, "Open File", "", "All Files (*)"
    )

            print(f"[DEBUG] File dialog returned: {file_path}")

            if file_path:
                with open(file_path, "r") as file:
                    data = file.read()
                print(f"[DEBUG] File content length: {len(data)} characters")

                print(f"[DEBUG] Import file number: {self.main_window.settingsBackend.mol_viewer_import_file_num}")

                if self.main_window.settingsBackend.mol_viewer_import_file_num == 0:
                    print("[DEBUG] Trying Chem.MolFromPDBBlock...")
                    output_file_path = "tab_backends/molecule_viewer_functions/molecule.pdb"
                    with open(output_file_path, "w") as file:
                        file.write(data)
                    self.main_window.moleculeViewerTab.update_display()
                    print("attempted update display and exiting funciton")
                   # print(f"[DEBUG] MolFromPDBBlock returned: {output}")
                    return data

                if self.main_window.settingsBackend.mol_viewer_import_file_num == 1:
                    print("[DEBUG] Trying Chem.MolFromMolBlock...")
                    output = Chem.MolFromMolBlock(data)
                    print(f"[DEBUG] MolFromMolBlock returned: {output}")

                if self.main_window.settingsBackend.mol_viewer_import_file_num == 2:
                    print("[DEBUG] Using Chem.SDMolSupplier...")
                    supplier = Chem.SDMolSupplier(data)  # multiple molecules
                    for m in supplier:
                        print(f"[DEBUG] SDMolSupplier molecule: {m}")
                        if m:  # None if parsing failed
                            print("[DEBUG] SMILES:", Chem.MolToSmiles(m))

                if self.main_window.settingsBackend.mol_viewer_import_file_num == 3:
                    print("[DEBUG] Trying Chem.MolFromInchi...")
                    output = Chem.MolFromInchi(data)
                    print(f"[DEBUG] MolFromInchi returned: {output}")

                if self.main_window.settingsBackend.mol_viewer_import_file_num == 4:
                    print("[DEBUG] Trying Chem.MolFromSmiles...")
                    output = Chem.MolFromSmiles(data)
                    print(f"[DEBUG] MolFromSmiles returned: {output}")

                if self.main_window.settingsBackend.mol_viewer_import_file_num == 5:
                    print("[DEBUG] Using Chem.TDTMolSupplier...")
                    supplier = Chem.TDTMolSupplier(data)
                    for mol in supplier:
                        print(f"[DEBUG] TDTMolSupplier molecule: {mol}")
                        if mol:
                            print("[DEBUG] SMILES:", Chem.MolToSmiles(mol))

                elif self.main_window.settingsBackend.mol_viewer_import_file_num == None:
                    print("[DEBUG] Falling back to Chem.MolFromPDBBlock...")
                    output = Chem.MolFromPDBBlock(data)
                    print(f"[DEBUG] MolFromPDBBlock returned: {output}")

                print("[DEBUG] Checking 'output' before AddHs...")
                try:
                    print(f"[DEBUG] output type: {type(output)}")
                except NameError:
                    print("[DEBUG] ERROR: 'output' is not defined!")
                    return
                try:
                    print("[DEBUG] Adding hydrogens...")
                    output = Chem.AddHs(output)
                    print("[DEBUG] Embedding molecule...")
                    AllChem.EmbedMolecule(output, AllChem.ETKDG())

                    print("[DEBUG] Converting to PDB block...")
                    pdb_output = Chem.MolToPDBBlock(output)
                    print(f"[DEBUG] PDB output length: {len(pdb_output)} characters")

                    output_file_path = "tab_backends/molecule_viewer_functions/molecule.pdb"
                    with open(output_file_path, "w") as file:
                        file.write(pdb_output)
                    print(f"[DEBUG] Wrote updated molecule to {output_file_path}")

                    print("[DEBUG] Updating display...")
                    self.main_window.moleculeViewerTab.update_display()
                    print("[DEBUG] Display updated successfully.")
                except Exception as e:
                    print(e)
                    print("moelcule could not be added at this time. please try again after cheking the file for errors or convert to pdb with openbabel and chnage your settings")
            else:
                print("[DEBUG] No file selected.")
                self.main_window.ui.PybraneShellDebugTextBox.append(
                    "WARNING: The file chosen is not the correct format or has not been picked."
                )

        except Exception as e:
            self.main_window.ui.PybraneShellDebugTextBox.append(
                    f"ERROR:{str(e)}"
                )
    def smiles_import(self):
        self.main_window.smilesdialog.show()

    def smiles_read(self):
        try:
            smiles_input = self.main_window.smilesdialog.molecularViewerSMILESInputField.text().strip()
            mol_input = Chem.MolFromSmiles(smiles_input)
            mol_input = Chem.AddHs(mol_input)
            AllChem.EmbedMolecule(mol_input, AllChem.ETKDG())
            output = Chem.MolToPDBBlock(mol_input)
                    
            with open("tab_backends/molecule_viewer_functions/molecule.pdb", "w") as file:
                file.write(output.strip())
            self.main_window.moleculeViewerTab.update_display()
        except Exception as e:
            self.main_window.ui.PybraneShellDebugTextBox.append(
                    f"ERROR:{str(e)}"
                )
    def start_atoms(self):
        self.main_window.atomdialog.show()

    def start_bonds(self):
        self.main_window.bonddialog.show()

    def manage_bonds(self):
        try:
            
            atom1 = self.main_window.bonddialog.MolecularViewerBondManagerAtom1SpinBox.value()
            atom2 = self.main_window.bonddialog.MolecularViewerBondManagerAtom2SpinBox.value()
            add_bond = self.main_window.bonddialog.MolecularViewerBondManagerAddRadioButton.isChecked()
            remove_bond = self.main_window.bonddialog.MolecularViewerBondManagerRemoveRadioButton.isChecked()
            index = self.main_window.bonddialog.MolecularViewerBondManagerTypeComboBox.currentIndex()
            text_options = ["Chem.rdchem.BondType.SINGLE", "Chem.rdchem.BondType.DOUBLE", "Chem.rdchem.BondType.TRIPLE", "Chem.rdchem.BondType.AROMATIC"]
            if 0 <= index < len(text_options):
                bond_choice = text_options[index]
            
            with open("tab_backends/molecule_viewer_functions/molecule.pdb", "r") as file:
                pdb_data = file.read()
            output = Chem.MolFromPDBBlock(pdb_data)
            rw_user_mol = Chem.RWMol(output)

            try:
                if add_bond and remove_bond:
                    self.main_window.ui.PybraneShellDebugTextBox.append(
                        "WARNING: You must pick one bond action, not both."
                    )
                if add_bond:
                    rw_user_mol.AddBond(atom1, atom2, order=bond_choice)
                if remove_bond:
                    bond = rw_user_mol.GetBondBetweenAtoms(atom1, atom2)
                    if bond:
                        rw_user_mol.RemoveBond(atom1, atom2)
                        print(f"Removed bond between atoms {atom1} and {atom2}")
                    else:
                        print("No bond found between the specified atoms.")
                else:
                    self.main_window.ui.PybraneShellDebugTextBox.append(
                        "WARNING: You must pick one bond action, not none"
                    )
                output = Chem.MolToPDBBlock(rw_user_mol)
                with open("tab_backends/molecule_viewer_functions/molecule.pdb", "w") as file:
                    file.write(output.strip())
                
                self.main_window.moleculeViewerTab.update_display()
            except Exception as e:
                print(e)
                self.main_window.ui.PybraneShellDebugTextBox.append(
                    "ERROR: The bond picked could not be updated."
                )
        except Exception as e:
           self.main_window.ui.PybraneShellDebugTextBox.append(
                    f"ERROR:{str(e)}"
                )
    def manage_atoms(self):
        try:
            atom1 = self.main_window.atomdialog.MolecularViewerAtomManagerIDSpinBox.value()
            add_atom = self.main_window.atomdialog.MolecularViewerAtomManagerAddRadioButton.isChecked()
            remove_atom = self.main_window.atomdialog.MolecularViewerAtomManagerRemoveRadioButton.isChecked()
            with open("tab_backends/molecule_viewer_functions/molecule.pdb", "r") as file:
                pdb_data = file.read()
            output = Chem.MolFromPDBBlock(pdb_data)
            rw_user_mol = Chem.RWMol(output)
            user_atom_index = self.main_window.atomdialog.MolecularViewerAtomManagerAtomicNumberSpinBox.value()

            try:
                if add_atom and remove_atom:
                    self.main_window.PybraneShellDebugTextBox.append(
                        "WARNING: You must pick one atom action, not both."
                    )
                if add_atom:
                    new_atom = Chem.Atom(user_atom_index)
                    rw_user_mol.AddAtom(new_atom)
                    self.main_window.ui.PybraneShellDebugTextBox.append(
                        f"Atom added at index: {rw_user_mol.GetNumAtoms() - 1}"
                    )
                if remove_atom:
                    rw_user_mol.RemoveAtom(user_atom_index)
                    self.main_window.ui.PybraneShellDebugTextBox.append(
                        f"Atom removed at index: {user_atom_index}"
                    )
                else:
                    self.main_window.ui.PybraneShellDebugTextBox.append(
                        "WARNING: You must pick one atom action, not none"
                    )
                output = Chem.MolToPDBBlock(rw_user_mol)
                with open("tab_backends/molecule_viewer_functions/molecule.pdb", "w") as file:
                    file.write(output.strip())
                
                self.main_window.moleculeViewerTab.update_display()
            except Exception as error:
                self.main_window.ui.PybraneShellDebugTextBox.append(
                    f"ERROR:{str(e)}")
                
        except Exception as e:
            self.main_window.ui.PybraneShellDebugTextBox.append(
                    f"ERROR:{str(e)}"
                )
    def manage_appearance(self):
        self.main_window.settingswindow.show()
        self.main_window.settingsdialog.SettingsTabWidget.setCurrentIndex(2)

    def file_settings(self):
        self.main_window.settingswindow.show()
        self.main_window.settingsdialog.SettingsTabWidget.setCurrentIndex(2)

    def load_examples(self):
        webbrowser.open('https://github.com/elusive-e/pybrane')