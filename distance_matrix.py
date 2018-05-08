#!/home/kmm5/anaconda2/bin/python
"""
 Calculates a distance matrix (contact map) for a cutoff.
 Author: Kareem Mehrabiani
 Date 7 May 2018

 For help, use -h option.
 usage: distance_matrix.py [-h] pdb_file cutoff

"""
import warnings
import argparse
import numpy as np
from Bio.PDB import *
from Bio.PDB.PDBParser import PDBParser
from Bio.PDB.PDBExceptions import PDBConstructionWarning
warnings.simplefilter('ignore', PDBConstructionWarning)

## Distance matrix function ##
def calc_residue_dist(residue_one, residue_two):
    """
    Returns the C-alpha distance between two residues
    """
    diff_vector = residue_one["CA"].coord - residue_two["CA"].coord
    return np.sqrt(np.sum(diff_vector * diff_vector))

def distance_matrix_calc(pdb_name, pdb_file, chain_letter, cutoff):
    """
    Distance function calculation
    """
    p = PDBParser(PERMISSIVE=1)
    structure = p.get_structure(pdb_name, pdb_file)
    model = structure[0]
    chain_I = model[chain_letter]
    chainsJ = structure.get_chains()

#    monomer_filename = 'distance_matrix_monomer_'+str(pdb_name)+'_'+ \
#            str(cutoff)+'.txt'
#    interface_filename = 'distance_matrix_interface_'+str(pdb_name)+'_'+ \
#            str(cutoff)+'.txt'
    monomer_filename = 'distance_matrix_monomer_'+str(cutoff)+'A_' \
            +str(pdb_name)
    interface_filename = 'distance_matrix_interface_'+str(cutoff)+'A_' \
            +str(pdb_name)
    monomer_file_out = open(monomer_filename, 'w')
    interface_file_out = open(interface_filename, 'w')

    # Initial parameters
    inter_predictions = 0
    mon_predictions = 0
    if (chain_letter != 'A'):
        for chain_J in chainsJ:
            for row, res_i in enumerate(chain_I) :
                for col, res_j in enumerate(chain_J) :
                    if (is_aa(res_i) == True and is_aa(res_j) == True) :
                        dist = calc_residue_dist(res_i, res_j)
                        if (dist <= cutoff):
                            if (chain_J != chain_I):
                                inter_predictions = inter_predictions + 1
                                interface_file_out.write("%d\t%d\t%f\n" \
                                        % (row+1, col+1, dist))
                            else:
                                mon_predictions = mon_predictions + 1
                                monomer_file_out.write("%d\t%d\t%f\n" \
                                        % (row+1, col+1, dist))
    else:
        for row, res_i in enumerate(chain_I) :
            for col, res_j in enumerate(chain_I) :
                if (is_aa(res_i) == True and is_aa(res_j) == True) :
                    dist = calc_residue_dist(res_i, res_j)
                    if (dist <= cutoff and dist > 0):
                        mon_predictions = mon_predictions + 1
                        monomer_file_out.write("%d\t%d\t%f\n"% \
                                (row+1, col+1, dist))

    print ("Monomer pairs: %d\nInterfacial pairs: %d\n" % \
            (mon_predictions, inter_predictions))
    print ("Wrote to two files:\n%s\n%s\n" % \
            (monomer_filename, interface_filename))

def main():
    """ Main function """
    parser = argparse.ArgumentParser(description='Calculates distance matrix \
            (contact map) at a cutoff. Outputs two files with monomer and \
            interface (if exists) residue pairs in the first two columns and \
            distance (in Angstroms) in the third column.')
    parser.add_argument('pdb_file', help='PDB file')
    parser.add_argument('chain_letter', help='Chain letter from which to \
            calculate distance matrix from. Important for calculating \
            interface pairs. If input file is a monomer, type the letter A.')
    parser.add_argument('cutoff', type=int, help='Cutoff for distance matrix \
            (in Angstroms).')
    args = parser.parse_args()

    pdb_file = args.pdb_file
    chain_letter = args.chain_letter
    cutoff = args.cutoff
    pdb_name = pdb_file
    distance_matrix_calc(pdb_name, pdb_file, chain_letter, cutoff=cutoff)

if __name__ == '__main__':
    main()
