import wikipedia 
from chemspipy import ChemSpider
import requests
class SearchAndFiles:
        def __init__(self, main_window):
            self.main_window = main_window
            self.cs = None
            
        def search_lipid_maps(self):
            self.pdb_request = self.main_window.ui.PybraneSearchQuearyLineEdit.text().strip()
            try:
                urls = []
                url = f"https://www.lipidmaps.org/rest/compound/pubchem_cid/{self.pdb_request}"
                urls.append(url)
                url = f"https://www.lipidmaps.org/rest/compound/formula/{self.pdb_request}/smiles"
                urls.append(url)
                url = f"https://www.lipidmaps.org/rest/compound/formula/{self.pdb_request}/pubchem_cid"
                urls.append(url)
                url = f"https://www.lipidmaps.org/rest/compound/formula/{self.pdb_request}/all"
                urls.append(url)
                url = f"https://www.lipidmaps.org/rest/compound/formula/{self.pdb_request}/molfile"
                urls.append(url)
                url = f"https://www.lipidmaps.org/rest/compound/smiles/{self.pdb_request}/all"
                urls.append(url)
                url = f"https://www.lipidmaps.org/rest/protein/uniprot_id/{self.pdb_request}/all"
                urls.append(url)
                url = f"https://www.lipidmaps.org/rest/protein/protein_name/{self.pdb_request}/all"
                urls.append(url)
                for url in urls:
                    response = requests.get(url)
                    data = response.json()
                    with open(f"{entry_id}.json", 'w') as file: # type: ignore
                        file.write(response.text)
                self.main_window.ui.PybraneFileTabDebugTextBox.append(f"Your lipid maps request yieled results saved in the file {entry_id}.json. Please be advised not all the results may be what you're looking for, as the query was ran through smiles, formula, and other ids, which will not match perfectly.") # type: ignore
            except:
                self.main_window.ui.PybraneFileTabDebugTextBox.append(f"ERROR: Your lipid maps search resulted in 0 results or encountered an error.")

        def search_chemspi(self):
            data = []
            pdb_request = self.main_window.ui.PybraneSearchQuearyLineEdit.text().strip()
            if self.cs == None:
                self.cs = ChemSpider('')
            r = self.cs.search(self.pdb_request)
            try:
                try:
                    chemspi = self.cs.get_compound(pdb_request)
                    data.append(chemspi.molecular_formula)
                    data.append(chemspi.molecular_weight)
                    data.append(chemspi.smiles)
                    
                    data.append(self.cs.search_by_mass)
                    data.append(self.cs.search_by_formula)
                    for i in range(len(data)):
                        with open(f"{entry_id}.json", 'w') as file: # type: ignore
                                file.write(data.text)
                    self.main_window.ui.PybraneFileTabDebugTextBox.append(f"Your Chem Spider request yieled results saved in the file {entry_id}.json. Please be advised not all the results may be what you're looking for, as the query was ran through smiles, formula, and other ids, which will not match perfectly. If it is the result your are lookign for, please save the file with a unique name so it is not overwritten if this query is searched again.") # type: ignore
                    # for result in self.cs.search(self.pdb_request):
                    #     with open(f"{entry_id}.json", 'w') as file:
                    #         file.write(result.text)
                    # data.append(r.message)
                except:
                    self.main_window.ui.PybraneFileTabDebugTextBox.append("ERROR: Your query did not return a result")
            
            except:
                self.main_window.ui.PybraneFileTabDebugTextBox.append(f"ERROR: Your Chem Spider request encountered an error or found 0 results. Please try again.")

        def search_pdb(self):
            try:
                self.pdb_request = self.main_window.PybraneSearchQuearyLineEdit.text().strip()
                url = f"https://files.rcsb.org/download/{self.pdb_request}.cif"

                url2 = f"https://data.rcsb.org/rest/v1/core/entry/{self.pdb_request}"

                response = requests.get(url2)

                data = response.json()
                data.keys()
                with open(f"{self.pdb_request}.cif", 'w') as file:
                    file.write(response.text)
                self.main_window.ui.PybraneFileTabDebugTextBox.append(f"Protein Data Bank Search resulted in a succesfu; retrival of info and structure. Structure file saved as {self.pdb_request}.cif")
            except:
                self.main_window.ui.PybraneFileTabDebugTextBox.append("ERROR: Your Protein Data BAnk Search resulted in 0 results or the search has encountered an error.")
        def search_wiki(self):
            self.pdb_request = self.main_window.ui.PybraneSearchQuearyLineEdit.text().strip()
            pdb_request = self.pdb_request
            try:
                output = wikipedia.summary(pdb_request)
            except:
                pdb_request = wikipedia.suggest(pdb_request)
                output = wikipedia.summary(pdb_request)
            self.main_window.ui.PybraneFileTabDebugTextBox.append(f"--> Wikipedia result for {pdb_request}:")
            self.main_window.ui.PybraneFileTabDebugTextBox.append(output)
        def update_cskey(self):
            self.cs = self.cs.SettingsSearchTabChemSpiKeyLineEdit.text.strip()