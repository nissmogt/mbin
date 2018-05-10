#!/home/kmm5/anaconda2/bin/python
"""

Solvent Accessible Surface Areas (SASA) filter script.

Author: Kareem Mehrabiani
Date: May 7th, 2018

usage: sasa_filter.py [-h] contact_file sasa_file N cutoff

INPUTS:
    contact_file: Ranked DCA pair list with three columns (i, j, DCA score)
    sasa_file: Residue list with two columns (residue, sasa ratio)
    N: number of DCA pairs to include in script
    cutoff: Number used to filter out residues that have a SASA ratio < cutoff.

OUTPUT:
    Four-column list of residue pairs, DCA score, and SASA ratio.

"""

import argparse
import numpy as np


def sasa_cutoff(contact_file, number_of_contacts, sasa_file, cutoff):
    """
    SASA cutoff filter function that takes inputs and uses the cutoff
    to filter out DCA pairs that have a SASA ratio < cutoff.
    """
    res_i, res_j, dca_score = np.loadtxt(contact_file, unpack=True)
    sasa_residue, sasa_ratio = np.genfromtxt(sasa_file, unpack=True, \
            usecols=(1,6), skip_header=1, skip_footer=10)
    sasa_dict = dict(zip(sasa_residue, sasa_ratio))

    out = []
    for i in range(len(res_i[:number_of_contacts])):
        try:
            if (sasa_dict[res_i[i]] >= cutoff or sasa_dict[res_j[i]] >= cutoff):
                out.append([res_i[i], res_j[i], dca_score[i], \
                        sasa_dict[res_i[i]], sasa_dict[res_j[i]]])
        except KeyError:
            print('Residue %d or %d not found in sasa file.\n' % \
                    (res_i[i], res_j[i]))

    numpy_array = np.array(out)
    index = 'residue_i\tresidue_j\tfn\tsasa_ratio_i\tsasa_ratio_j'
    np.savetxt(contact_file+'_sasa_'+str(cutoff), numpy_array, \
            fmt='%d\t%d\t%.5f\t%.2f\t%.2f', header=index)

    print "DCA pairs > SASA cutoff: %d%%\n" % \
            (len(out)/float(number_of_contacts)*100)

def main():
    """
    Main function that calls sasa_cutoff function and defines inputs.
    """

    # Used to pass arguments from terminal to this script
    parser = argparse.ArgumentParser(description="Filters out DCA contacts \
            with Solvent Accessible Surface Areas (SASA) ratio less than \
            cutoff (SASA is calculated from GetArea Server).")
    parser.add_argument('dca_file', help='Ranked and PDB-mapped DCA pair list \
            with DCA score in the third column (res i, res j, DCA score).')
    parser.add_argument('sasa_file', help='A list of residues and their \
            corresponding SASA ratio percentage in the second column \
            (residue, SASA ratio).')
    parser.add_argument('N', type=int, help='Number of DCA pairs to filter.')
    parser.add_argument('CUTOFF', type=int, help='SASA ratio cutoff.')

    args = parser.parse_args()

    dca_file = args.dca_file
    sasa_file = args.sasa_file
    number_of_contacts = args.N
    cutoff = args.CUTOFF
    sasa_cutoff(dca_file, number_of_contacts, sasa_file, cutoff)

if __name__ == '__main__':
    main()
