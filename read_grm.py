import numpy as np
import struct
import os

def read_individuals(ind_file):
    inds = {}
    with open(ind_file) as T:
        c = 1
        for line in T:
            inds[c] = line.strip().replace('\t', '_')
            c +=1
    return inds 

def read_grm_bin(file_path, n_individuals):
    """
    Read the GRM binary file.
    
    Parameters:
    - file_path: Path to the .bin file.
    - n_individuals: Number of individuals in the GRM.
    
    Returns:
    - grm_matrix: The GRM as a NumPy array.
    """
    # The number of elements in the upper triangle of the GRM
    n_elements = (n_individuals * (n_individuals + 1)) // 2

    # Check the expected file size
    expected_size = n_elements * 4  # 4 bytes per float
    
    actual_size = os.path.getsize(file_path)
    
    if expected_size != actual_size:
        raise ValueError(f"File size mismatch: expected {expected_size} bytes but got {actual_size} bytes.")
    
    # Read the binary file
    with open(file_path, "rb") as file:
        grm_data = file.read()
    
    # Ensure the data buffer is the correct size
    if len(grm_data) != expected_size:
        raise struct.error(f"Buffer size mismatch: expected {expected_size} bytes but got {len(grm_data)} bytes.")
    
    # Unpack the binary data into a numpy array
    grm_matrix = np.array(struct.unpack(f"{n_elements}f", grm_data), dtype=float)
    
    # Reshape the array to be a square matrix
    grm_full = np.zeros((n_individuals, n_individuals))
    grm_full[np.triu_indices(n_individuals)] = grm_matrix
    grm_full += np.triu(grm_full, 1).T  # Reflect to lower triangle
    
    return grm_full

def print_individual_scores(grm_matrix, inds_dict):
    n_individuals = grm_matrix.shape[0]
    
    for i in range(n_individuals):
        for j in range(i, n_individuals):  # Iterate only over the upper triangle (including the diagonal)
            score = grm_matrix[i, j]
            if score >=0.9 and score <= 1.6:
                print(f"Individual {inds_dict[i+1]} vs Individual {inds_dict[j+1]}: {score:.6f}")

grm_path = '/home/edizadehm/02.tutorials/07.gcta/SCZ_Fam_data/SCZ_Fam_autosomes.grm.bin'
ind_path = '/home/edizadehm/02.tutorials/07.gcta/SCZ_Fam_data/SCZ_Fam_autosomes.grm.id'
inds = read_individuals(ind_path)
n_individuals = len(inds)  
try:
    grm_matrix = read_grm_bin(grm_path, n_individuals)
    print_individual_scores(grm_matrix, inds)
    # print(grm_matrix)
except Exception as e:
    print(f"Error reading GRM file: {e}")