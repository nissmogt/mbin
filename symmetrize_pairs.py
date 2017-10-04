#!/home/kmm5/anaconda2/bin/python

######################################################################
#   Given a residue pair, *i* and *j*, that is an interchain contact,
#   this function makes it so that residue ***i*** is also in contact
#   with every residue ***j*** for each chain.
#
######################################################################
import numpy as np
import sys
import string
from Bio.PDB import *
from Bio.PDB.PDBParser import PDBParser
import warnings
from Bio.PDB.PDBExceptions import PDBConstructionWarning
warnings.simplefilter('ignore', PDBConstructionWarning)

pdbID = '2zwh'
pdb_file = '/home/kmm5/actin/factin/oda9.pdb'
# pdb_file = '/home/kmm5/mreb/sbm/mamk/5ljv_mamk.pdb'
# pdb_file = '/home/kmm5/hsp70/4jne.pdb'
# dca_contacts = np.loadtxt('/home/kmm5/actin/pdb_interfacial_6A.contacts')

#dca_contacts = np.loadtxt('/home/kmm5/actin/plmDCA/dca12A_inter_pfam.contacts')
#dca_contacts = np.loadtxt('/home/kmm5/actin/plmDCA/cytoplasm/from_actin-actin_subseq/dca12A_inter_actin2.contacts')
dca_contacts = np.loadtxt('/home/kmm5/actin/plmDCA/cytoplasm/from_actin-actin_subseq/one_interface.contacts')

# dca_contacts = np.loadtxt('/home/kmm5/mreb/plmdca/mreb_single/mamk_mapped.fn')
# dca_contacts = np.loadtxt('/home/kmm5/hsp70/plmdca/hsp70_swiss_mapped.fn')

## Creates a dictionary of characters (from A-Z) to corresponding numbers
def genChainDict(chain_length):
    chain_dict = {}
    chain_numbers = range(chain_length)
    chain_letters = []
    for char in string.ascii_uppercase:
        chain_letters.append(char)

    chain_dict = dict(zip(chain_letters, chain_numbers))
    return chain_dict

## MAIN FUNCTION
def genInterfaceDCA(dca_contacts, total_dca_pairs, nres=374, nchain=None):
    
    # Initial parameters
    total_generated = 0
    missing_res = 0
    
    # Extract PDB information using BIOpython
    p = PDBParser(PERMISSIVE=1)
    structure = p.get_structure(pdbID, pdb_file)
    
    chain_length = len(Selection.unfold_entities(structure, 'C'))
    if nchain is None:
        nchain = chain_length
    chain_dict = genChainDict(nchain)
    
    target = open('DCAsym.contacts', 'w')
    expected_pairs = total_dca_pairs*nchain*(nchain-1)   
    # Loop thru each DCA pair for each Chain in PDB and calculate pair distances
    for pair in dca_contacts[0:total_dca_pairs]:
        i = int(pair[0])
        j = int(pair[1])
        chainsI = structure.get_chains()
        
        # Need this try/except statement in case there are missing residues in PDB
        try:    
            #for chain_I in tuple(chainsI)[0:nchain]:
            chain_I = tuple(chainsI)[4]
            chainsJ = structure.get_chains()
            for chain_J in tuple(chainsJ)[0:nchain]:
                if (chain_J != chain_I):
#                         res_i = chain_I[i]
#                         res_j = chain_J[j]
#                         dist = abs(res_i['CA'] - res_j['CA'])
                    chain_I_offset = nres*chain_dict.get(chain_I.id)
                    chain_J_offset = nres*chain_dict.get(chain_J.id)

                    if (chain_I.id == 'E' and chain_J.id == 'D'):
                        target.write("%d\t%d\n" % (i + chain_I_offset, j + chain_J_offset))
                        
                    total_generated += 1

        except TypeError:
            print("\n** TypeError encountered: **")
            print("   CHAINS %s and %s DO NOT EXIST or CANNOT BE ACCESSED." 
                  % (chain_I.id, chain_J.id))
            
    target.close()
    print("DCA pairs: %d" % total_dca_pairs)
    print("CHAINS: %d" % nchain)
    print("ACTUAL   symmetrized DCA pairs: %d" % total_generated)
    print("EXPECTED symmetrized DCA pairs: %d\n" % expected_pairs)

## RUN SCRIPT
total_dca_pairs = 10
genInterfaceDCA(dca_contacts, total_dca_pairs, nres=371)

