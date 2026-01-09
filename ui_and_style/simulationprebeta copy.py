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
import sys
import re
import subprocess
import json
#import pdbfixer
import requests
from rdkit.Chem import rdDepictor as rdd
from rdkit.Chem.Draw import rdMolDraw2D as draw2D
from rdkit import Chem
from rdkit.Chem.Draw import DrawingOptions
from rdkit.Chem import Draw, AllChem

class SimulationBackend:
    def __init__(self, main_window):
        self.main_window = main_window
        self.amber_in_path = None
        self.amber_prm_path = None

    def starts_simulation(self):
        inpcrd = AmberInpcrdFile(f"{self.amber_in_path}")
        prmtop = AmberPrmtopFile(f"{self.amber_prm_path}", periodicBoxVectors=inpcrd.boxVectors)
        system = prmtop.createSystem(nonbondedMethod=PME, nonbondedCutoff=1*nanometer,
        constraints=constraint_choice)
        
        constraint_index = self.main_window.ui.PybraneSimSetUpBondComboBox.currentIndex()
        constraint_set = ["None", "SHAKE", "HBonds","AllBonds"]
        if 0 <= constraint_index < len(constraint_set):
            constraint_choice = constraint_set[constraint_index]
        # thermostat_index = self.main_window.ui.PybraneSimSetUpBondComboBox.currentIndex()
        # thermostat_set = ["None", "Berendsen", "Langevin","Langevin"]
        # if 0 <= thermostat_index < len(thermostat_set):
        #     thermostat_choice = thermostat_set[thermostat_index]
        
        step_size = f"{int(self.main_window.ui.PybraneSimSetUpTimeStepLineEdit.strip())}*picoseconds"
        ensemble_index = self.main_window.ui.PybraneSimSetUpEnsembleComboBox.currentIndex()
        user_temp = f"{int(self.main_window.ui.PybraneSimSetUpTempLineEdit.strip())}*kelvin"
        user_press = self.main_window.ui.PybraneSimSetUpPressLineEdit.strip()
        if ensemble_index == 0:#nve
            integrator = VerletIntegrator(step_size)
        if ensemble_index == 1:#nvt
            if intr_index == 1:
                integrator = BrownianIntegrator(user_temp, 1/picosecond, step_size)
            if intr_index == 2:
                integrator = LangevinMiddleIntegrator(user_temp, 1/picosecond, step_size)
            if intr_index == 3:
                system.addForce(AndersenThermostat(user_temp, 1/picosecond))
                integrator = VerletIntegrator(step_size)
            if intr_index == 4:
                integrator = NoseHooverIntegrator(user_temp, 1/picosecond,step_size)
        if ensemble_index == 2:#npt
            baro_index = self.main_window.ui.PybraneSimSetUpBArostatComboBox.currentIndex()
            intr_index = self.main_window.ui.PybraneSimSetUpThermostatComboBox.currentIndex()
            if baro_index == 1:
                system.addForce(MonteCarloBarostat(1*bar, user_press))
            if baro_index == 2:
                system.addForce(MonteCarloAnisotropicBarostat((1, 1, 2)*bar, user_press))
            if intr_index == 1:
                integrator = BrownianIntegrator(user_temp, 1/picosecond, step_size)
            if intr_index == 2:
                integrator = LangevinMiddleIntegrator(user_temp, 1/picosecond, step_size)
            if intr_index == 3:
                system.addForce(AndersenThermostat(user_temp, 1/picosecond))
                integrator = VerletIntegrator(step_size)
            if intr_index == 4:
                integrator = NoseHooverIntegrator(user_temp, 1/picosecond,step_size)

        system = prmtop.createSystem(nonbondedMethod=NoCutoff, constraints=constraint_set)

        simulation = Simulation(prmtop.topology, system, integrator)
        simulation.context.setPositions(inpcrd.positions)
        simulation.minimizeEnergy()
        
        simulation_step = int(self.main_window.ui.PybraneSimSetUpProductionLineEdit.strip())
        simulation_time = int(self.main_window.ui.PybraneSimSetUpSimTimeLineEdit.strip())
        save_time_step = int(self.main_window.ui.PybraneSimSetUpSaveTimeStepLineEdit.strip())
        simulation.reporters.append(DCDReporter('output.dcd', save_time_step))
        simulation.reporters.append(StateDataReporter(stdout, save_time_step, step=True,
                potentialEnergy=True, temperature=True))
        simulation.step(simulation_time)

    # def start_simulation(self):
    #     forcefield = self.main_window.simulationTab.forcefield
    #     pdb = self.main_window.simulationTab.pdb

    #     self.main_window.PybraneSimSetUpDebugTextBox.append(f"NOTICE: The simulation was started. Inputs: {pdb, forcefield}")
    #     try:
    #         modeller = Modeller(pdb.topology, pdb.positions)
    #         membrane = self.main_window.simulationTab.mem

    #         if membrane is None:
    #             self.main_window.PybraneSimSetUpDebugTextBox.append("NOTICE: No membrane selected, creating a default.")
    #             modeller.addMembrane(forcefield, lipidType='POPC', minimumPadding=1 * nanometer) # type: ignore
    #         else:
    #             modeller.add(membrane.topology, membrane.positions)
    #             modeller.addSolvent(forcefield, model='tip3p', padding=1.0 * nanometers) # type: ignore

    #         print(f"Number of atoms in topology: {pdb.topology.atoms()}")
    #         print(f"Number of positions: {pdb.positions}")
    #         self.main_window.PybraneSimSetUpDebugTextBox.append("NOTICE: The modeller was created.")

    #         system = forcefield.createSystem(
    #             modeller.topology,
    #             nonbondedMethod=PME,
    #             nonbondedCutoff=1 * nanometer, # type: ignore
    #             constraints=HBonds
    #         )

    #         self.main_window.PybraneSimSetUpDebugTextBox.append("NOTICE: The system was created.")
    #         print(f"Number of atoms in modeller: {modeller.topology.getNumAtoms()}")
    #         print(f"Number of particles in system: {system.getNumParticles()}")

    #         integrator = LangevinIntegrator(300 * kelvin, 1 / picosecond, 0.002 * picoseconds) # type: ignore
    #         self.main_window.PybraneSimSetUpDebugTextBox.append("NOTICE: The integrator was created.")

    #         simulation = Simulation(modeller.topology, system, integrator)
    #         self.main_window.PybraneSimSetUpDebugTextBox.append("NOTICE: The simulation was created.")

    #         simulation.context.setPositions(modeller.positions)
    #         self.main_window.PybraneSimSetUpDebugTextBox.append("NOTICE: The positions were set.")

    #         simulation.minimizeEnergy()
    #         self.main_window.PybraneSimSetUpDebugTextBox.append("NOTICE: Energy was minimized.")

    #         simulation.context.setVelocitiesToTemperature(300 * kelvin)
    #         self.main_window.PybraneSimSetUpDebugTextBox.append("NOTICE: The temperature was set.")

    #         simulation.reporters.append(StateDataReporter(stdout, 1000, step=True, potentialEnergy=True, temperature=True))
    #         simulation.reporters.append(DCDReporter('trajectory.dcd', 1000))

    #         self.main_window.PybraneSimSetUpDebugTextBox.append("NOTICE: The simulation is running...")

    #         simulation.step(10000)
    #         positions = simulation.context.getState(getPositions=True).getPositions()

    #         with open('output.pdb', 'w') as output_file:
    #             PDBFile.writeFile(simulation.topology, positions, output_file)

    #         self.main_window.PybraneSimSetUpDebugTextBox.append("NOTICE: The simulation is finished.")
    #     except Exception as e:
    #         self.main_window.PybraneSimSetUpDebugTextBox.append(f"ERROR: {e}")

    def load_forcefield(self):
        default_forcefield = ForceField('charmm36.xml', 'charmm36/water.xml')
        self.main_window.simsim.forcefield = default_forcefield
        self.main_window.ui.PybraneSimSetUpDebugTextBox.append("NOTICE: Default forcefield loaded. Choose custom or cancel to use default.")

        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self.main_window, "Open Forcefield File", "", "All Files (*)")
        if file_path:
            with open(file_path, 'r') as file:
                _ = file.read()
            forcefield = ForceField(file_path)
            self.main_window.simsim.forcefield = forcefield
            self.main_window.ui.PybraneSimSetUpDebugTextBox.append("Forcefield file was successfully loaded.")
        else:
            self.main_window.ui.PybraneSimSetUpDebugTextBox.append("WARNING: Invalid file selected. Default forcefield will be used.")

    def load_protein_structure(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self.main_window, "Open Protein PDB File", "", "All Files (*)")
        if file_path:
            fixer = PDBFixer(file_path)
            fixer.findMissingResidues()
            fixer.findMissingAtoms()
            fixer.addMissingAtoms()
            fixer.addMissingHydrogens()

            with open('fixed_structure.pdb', 'w') as f:
                PDBFile.writeFile(fixer.topology, fixer.positions, f)

            pdb = PDBFile('fixed_structure.pdb')
            self.main_window.simsim.pdb = pdb
            self.main_window.PybraneSimSetUpDebugTextBox.append("Protein structure successfully loaded.")
        else:
            self.main_window.PybraneSimSetUpDebugTextBox.append("WARNING: Invalid or no file selected.")

    def load_membrane_structure(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self.main_window, "Open Membrane File", "", "All Files (*)")
        if file_path:
            fixer = PDBFixer(file_path)
            self.main_window.PybraneSimSetUpDebugTextBox.append("Fixer activated :)")
            fixer.findMissingResidues()
            self.main_window.PybraneSimSetUpDebugTextBox.append("Found missing residues :)")
            fixer.findMissingAtoms()
            self.main_window.PybraneSimSetUpDebugTextBox.append("Found missing atoms :)")
            fixer.addMissingAtoms()
            self.main_window.textBrPybraneSimSetUpDebugTextBoxowser_13.append("Added missing atoms :)")
            # fixer.addMissingHydrogens()
            self.main_window.PybraneSimSetUpDebugTextBox.append("Added hydrogens! :)")

            with open('fixed_mem_structure.pdb', 'w') as f:
                PDBFile.writeFile(fixer.topology, fixer.positions, f)

            membrane = PDBFile('fixed_mem_structure.pdb')
            self.main_window.simsim.mem = membrane
            self.main_window.ui.PybraneSimSetUpDebugTextBox.append("Membrane file successfully loaded.")
        else:
            self.main_window.PybraneSimSetUpDebugTextBox.append("WARNING: Invalid or no file selected.")

    def load_macromolecule_structure(self):
    #TODO: add logic for "other" files
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self.main_window, "Open Macromolecule File", "", "All Files (*)")
        if file_path:
            macro = PDBFile(file_path)
            self.additional_macromolecules.append(macro)
            self.main_window.simsim.macro_other = self.additional_macromolecules
            self.main_window.PybraneSimSetUpDebugTextBox.append("Macromolecule file successfully loaded.")
        else:
            self.main_window.PybraneSimSetUpDebugTextBox.append("WARNING: Invalid or no file selected.")

    def load_in(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self.main_window, "Open Solvent File", "", "All Files (*)")
        if file_path:
            self.amber_in_path = file_path
            self.main_window.PybraneSimSetUpDebugTextBox.append("Solvent file successfully loaded.")
        else:
            self.main_window.PybraneSimSetUpDebugTextBox.append("WARNING: Invalid or no file selected.")
            
    def load_prm(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self.main_window, "Open Solvent File", "", "All Files (*)")
        if file_path:
            self.amber_prm_path = file_path
            self.main_window.PybraneSimSetUpDebugTextBox.append("Solvent file successfully loaded.")
        else:
            self.main_window.PybraneSimSetUpDebugTextBox.append("WARNING: Invalid or no file selected.")
    
    
    def update_3d_display(self):
        with open("tab_backends/molecule_viewer_functions/membrane_generator_settings.json", "r") as file:
            settings = json.load(file)
        with open("tab_backends/molecule_viewer_functions/membrane_output_3D.pdb", "r") as file:
            pdb_data = file.read()
            if not pdb_data.strip():  # also ignores whitespace-only files
                print("File is blank")
            else:
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
                self.main_window.ui.PybraneSimSetUp3DJSViewer.page().runJavaScript(js_code)