class MembraneMakerBackend:
    def __init__(self, main_window):
        self.bilayer_generator = membrane_generator_master(self)
        self.protein_embedder = protein_inserter_master(self)

        self.lipid_structure_paths = []
        self.lipid_structure_ratios = []

        self.num_lipids_x = None
        self.num_lipids_y = None
        self.box_height = None
        self.lipid_spacing = None
        self.membrane_dimensions = None

        self.generated_membrane_path = 'membrane_maker_output.pdb'
        self.final_box_height = None
        self.use_protein_embedding = None
        self.output_structure_path = 'membrane_maker_output.pdb'

        self.protein_spacing_factor = None
        self.protein_structure_paths = []
        self.protein_rotation_matrices = []

    def generate_membrane(self):
        self.num_lipids_x = window.x_spin_box.value()
        self.num_lipids_y = window.y_spin_box.value()
        self.box_height = window.z_spin_box.value()
        self.lipid_spacing = window.spacing_spin.value()
        self.membrane_dimensions = (self.num_lipids_x, self.num_lipids_y, self.box_height)
        self.generated_membrane_path = 'membrane_maker_output.pdb'
        self.final_box_height = window.final_z_spin.value()
        self.use_protein_embedding = window.radioButton.isChecked()
        self.output_structure_path = 'membrane_maker_output.pdb'
        self.protein_structure_paths = []
        self.protein_rotation_matrices = []
        self.protein_spacing_factor = window.pro_spin_ratio.value()

        window.textBrowser_7.append("Initialized membrane build parameters.")
        window.textBrowser_7.append("Lipid structures:", self.lipid_structure_paths)
        window.textBrowser_7.append("Lipid ratios:", self.lipid_structure_ratios)
        window.textBrowser_7.append("Output PDB:", self.output_structure_path)
        window.textBrowser_7.append("Lipids in X:", self.num_lipids_x)
        window.textBrowser_7.append("Lipids in Y:", self.num_lipids_y)
        window.textBrowser_7.append("Spacing between lipids:", self.lipid_spacing)
        window.textBrowser_7.append("Initial box height (Z):", self.box_height)
        window.textBrowser_7.append("Final box height (Z):", self.final_box_height)
        window.textBrowser_7.append("Lipid ratio list:", self.lipid_structure_ratios)

        if not self.use_protein_embedding:
            try:
                self.bilayer_generator.generate_bilipid_membrane(
                    self.lipid_structure_paths,
                    self.lipid_structure_ratios,
                    self.output_structure_path,
                    self.num_lipids_x,
                    self.num_lipids_y,
                    self.lipid_spacing,
                    self.box_height,
                    self.final_box_height
                )
                window.textBrowser_7.append("Membrane generation complete.")
            except:
                window.textBrowser_7.append("ERROR: Membrane generation failed. Check all inputs.")
        else:
            try:
                self.bilayer_generator.generate_bilipid_membrane(
                    self.lipid_structure_paths,
                    self.lipid_structure_ratios,
                    self.output_structure_path,
                    self.num_lipids_x,
                    self.num_lipids_y,
                    self.lipid_spacing,
                    self.box_height,
                    self.final_box_height
                )
                self.protein_embedder.orient_proteins_in_membrane(
                    self.protein_structure_paths,
                    self.generated_membrane_path,
                    self.output_structure_path,
                    self.protein_rotation_matrices,
                    self.membrane_dimensions,
                    self.protein_spacing_factor
                )
            except:
                window.textBrowser_7.append("ERROR: Protein insertion or membrane generation failed.")

    def import_lipid_structure(self):
        ratio_input = window.memratiospin.value()
        if ratio_input == 0 or ratio_input >= 1.0:
            window.textBrowser_7.append("WARNING: Lipid ratio must be between 0 and 1.")
        else:
            try:
                self.lipid_structure_ratios.append(float(ratio_input))

                structure_path, _ = QtWidgets.QFileDialog.getOpenFileName(window, "Open Lipid File", "", "All Files (*)")
                if structure_path:
                    with open(structure_path, 'r') as file:
                        file_content = file.read()

                if file_content not in self.lipid_structure_paths:
                    self.lipid_structure_paths.append(str(structure_path))
                    window.textBrowser_7.append(
                        f"Imported lipid: {structure_path} with ratio: {ratio_input}"
                    )
            except:
                window.textBrowser_7.append("ERROR: Failed to import lipid structure.")

    def import_protein_structure(self):
        if self.use_protein_embedding:
            try:
                protein_path, _ = QtWidgets.QFileDialog.getOpenFileName(window, "Open Protein File", "", "All Files (*)")
                if protein_path:
                    self.protein_structure_paths.append(protein_path)
            except:
                window.textBrowser_7.append("ERROR: Failed to load protein file. Please verify the file format.")
