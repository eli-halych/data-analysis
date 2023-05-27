# %% Load dataset
import pandas as pd
DATA_PATH = './data/raw/HIV.csv'
data = pd.read_csv(DATA_PATH)
data.head()

# %% general information about the dataset
print(data.shape)
print(data["HIV_active"].value_counts())

# %% Show sample molecules
import rdkit
from rdkit import Chem
from rdkit.Chem import Draw

sample_smiles = data["smiles"][4:30].values
sample_mols = [Chem.MolFromSmiles(smile) \
                for smile in sample_smiles]
grid = Draw.MolsToGridImage(sample_mols, 
                            molsPerRow=4, 
                            subImgSize=(200, 200))

grid
# %% Create a dataset
import torch
from torch.utils.data import Dataset, Data
import numpy as np
import os
from rdkit.Chem import rdmolops
from tqdm import tqdm
import os.path as osp


class MoleculeDataset(Dataset):
    def __init__(self, root, transform=None, pre_transform=None, pre_filter=None):
        """Dataset for molecules.

        Args:
            root: where to save the dataset.
            transform: Defaults to None.
            pre_transform: Defaults to None.
            pre_filter: Defaults to None.
        """
        super().__init__(root, transform, pre_transform, pre_filter)

    @property
    def raw_file_names(self):
        return ["HIV.csv"]

    @property
    def processed_file_names(self):
        """Return the file names of the processed data.

        Raises:
            NotImplementedError.
        """
        raise NotImplementedError("Not Implemented.")

    def download(self):
        """Download to `self.raw_dir`."""
        pass

    def process(self):
        """Process the dataset to `self.processed_dir`."""
        self.data = pd.read_csv(self.raw_paths[0])
        for index, mol in tqdm(self.data.iterrows(), total=self.data.shape[0]):
            mol_obj = Chem.MolFromSmiles(mol["smiles"])
            
            node_feats = self._get_node_features(mol_obj)
            edge_feats = self._get_edge_features(mol_obj)
            edge_index = self._get_adjacency_info(mol_obj)
            label = self._get_labels(mol["HIV_active"])

            data = Data(x=node_feats, 
                        edge_index=edge_index,
                        edge_attr=edge_feats,
                        y=label,
                        smiles=mol["smiles"]
                        ) 
            
            torch.save(data, 
                    os.path.join(self.processed_dir, 
                                 f'data_{index}.pt'))
            
    def _get_node_features(self, mol):
        """ Node features are the atom features.

        Args:
            mol: rdkit mol object.

        Returns: a matrix / 2d array of the shape 
                 [Number of Nodes, Node Feature size].
        """
        all_node_feats = []

        for atom in mol.GetAtoms():
            node_feats = []
            # Feature 1: Atomic number        
            node_feats.append(atom.GetAtomicNum())
            # Feature 2: Atom degree
            node_feats.append(atom.GetDegree())
            # Feature 3: Formal charge
            node_feats.append(atom.GetFormalCharge())
            # Feature 4: Hybridization
            node_feats.append(atom.GetHybridization())
            # Feature 5: Aromaticity
            node_feats.append(atom.GetIsAromatic())
            # Feature 6: Total Num Hs
            node_feats.append(atom.GetTotalNumHs())
            # Feature 7: Radical Electrons
            node_feats.append(atom.GetNumRadicalElectrons())
            # Feature 8: In Ring
            node_feats.append(atom.IsInRing())
            # Feature 9: Chirality
            node_feats.append(atom.GetChiralTag())

            # Append node features to matrix
            all_node_feats.append(node_feats)

        all_node_feats = np.asarray(all_node_feats)
        return torch.tensor(all_node_feats, dtype=torch.float)

    def _get_edge_features(self, mol):
        """ Edge features are the bond features.

        Args:
            mol: rdkit mol object.

        Returns: a matrix / 2d array of the shape 
                 [Number of edges, Edge Feature size].
        """
        all_edge_feats = []

        for bond in mol.GetBonds():
            edge_feats = []
            # Feature 1: Bond type (as double)
            edge_feats.append(bond.GetBondTypeAsDouble())
            # Feature 2: Rings
            edge_feats.append(bond.IsInRing())
            # Append node features to matrix (twice, per direction)
            all_edge_feats += [edge_feats, edge_feats]

        all_edge_feats = np.asarray(all_edge_feats)
        return torch.tensor(all_edge_feats, dtype=torch.float)
    
    def _get_adjacency_info(self, mol):
        """ Get the adjacency information of the molecule.

        Args:
            mol: rdkit mol object.

        Returns:
            edge_indices
        """
        edge_indices = []
        for bond in mol.GetBonds():
            i = bond.GetBeginAtomIdx()
            j = bond.GetEndAtomIdx()
            edge_indices += [[i, j], [j, i]]

        edge_indices = torch.tensor(edge_indices)
        edge_indices = edge_indices.t().to(torch.long).view(2, -1)
        return edge_indices

    def _get_labels(self, label):
        """Get the label of the molecule.

        Args:
            label: the label of the molecule.

        Returns:
            torch.tensor of the label.
        """
        label = np.asarray([label])
        return torch.tensor(label, dtype=torch.int64)

    def len(self):
        return len(self.processed_file_names)

    def get(self, idx):
        data = torch.load(osp.join(self.processed_dir, f'data_{idx}.pt'))
        return data



# %% Test the dataset creation
dataset = MoleculeDataset(root='./data/')

# %%
print(dataset[0].edge_index.t())
print(dataset[0].x)
print(dataset[0].edge_attr)
print(dataset[0].y)
