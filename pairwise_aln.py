#!/home/kmm5/anaconda2/bin/python

import numpy as np
def backmap(pfamfile, pdbfile):
    import re
    from Bio import pairwise2
    from Bio.pairwise2 import format_alignment
    l = []
    pfamopen = open(pfamfile, "r")
    for line in pfamopen:
        l.append(line)
    header = l[0]
    pfamseq = l[1]

    l2 = []
    pdbopen = open(pdbfile, "r")
    for line2 in pdbopen:
        l2.append(line2)
    header_pdb = l2[0]
    pdbseq = l2[1]

    alignments = pairwise2.align.globalxx(pfamseq, pdbseq)
    print(format_alignment(*alignments[0]))
    fastastart = re.search("[A-Z]", alignments[0][1]).start()
    pdbstart = re.search("[A-Z]", alignments[0][0]).start()
    N = min(len(pfamseq),len(pdbseq))
    pdb_indices = range(pdbstart,N+pdbstart)
    dca_indices = range(fastastart,N+fastastart)
    map_to_dca = dict(zip(pdb_indices, dca_indices))
    map_to_pdb = dict(zip(dca_indices, pdb_indices))
    return map_to_dca
###############################################################################
def map_dca(pfamfile, pdbfile, dcafile):
    import os
    """Converts DCA pairs into PDB coordinates and outputs a file."""
    name = os.path.split(dcafile)[-1]
    col_name = ['i', 'j', 'score']
    dca_data = np.genfromtxt(dcafile,names=col_name, dtype=None, \
            usecols=(0,1,2))
    outfile_map = "map_"+name
    map_dict = backmap(pfamfile, pdbfile)
    N = len(dca_data)
    mapped_dca = []
    for i in range(N):
        dca_resi = dca_data['i'][i]
        dca_resj = dca_data['j'][i]
        fn = dca_data['score'][i]
        if dca_resi in map_dict and dca_resj in map_dict:
            mapped_dca.append([map_dict[dca_resi], map_dict[dca_resj], fn, \
                dca_resi, dca_resj])

    header = 'i\tj\tfn\ti_pfam\tj_pfam'
    np.savetxt(outfile_map, mapped_dca, fmt='%d\t%d\t%f\t%d\t%d', header=header)

################################################################################
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Aligns an MSA to PDB \
            sequence.")
    parser.add_argument('--dca', help='DCA three-column contact map.')
    parser.add_argument('--pfam', help='A single sequence from MSA that\
            has same Uniprot ID as PDB.')
    parser.add_argument('--pdb', help='Sequence from PDB. If two \
            chains, add second to first.')

    args = parser.parse_args()
    dcafile = args.dca
    pfamfile = args.pfam
    pdbfile = args.pdb

    map_dca(pfamfile, pdbfile, dcafile)
    
if __name__ == '__main__':
    main()
