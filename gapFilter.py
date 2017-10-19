#!/home/kmm5/anaconda2/bin/python
"""
Author: Kareem Mehrabiani
Date: 17 October 2017

usage: gapFilter.py [-h] [-gf] msa_file gap_threshold

Filters sequences of a Multiple-Sequence Alignment, given fraction of gaps (-)
present.

positional arguments:
  msa_file       Multiple-Sequence Alignment file
  gap_threshold  Gap threshold (from 0 to 1.0) Default=0.25

optional arguments:
  -h, --help     show this help message and exit
  -gf            Outputs a file containing the fraction of gaps for each
                 sequence.

"""

import numpy as np
from Bio import AlignIO
from Bio import SeqIO
from Bio.Seq import Seq
import argparse


def gap_filter(msa_input, gap_threshold=0.25, output_gaps=False):
    """
    First removes insertions (.) and lowercase letters, if there are any.
    Then counts the number of gaps in each sequence and from this,
    calculates the fraction of gaps present. If this fraction is greater
    than the input gap threshold (Default=0.25), then that
    particular sequence is thrown out. Optional: Gap percent per sequence
    can be returned (by output_gaps=True).
    """
    print('================================================================')
    print('Use gapFilter.py -h or --help for usage.')
    print('Gap threshold is %2.d%%.\n' % (gap_threshold*100))
    length_sequence = 375
    alignment = AlignIO.read(msa_input, 'fasta')
    total_sequences= len(alignment)


    output_handle = open(msa_input.name + '_filtered_%dp' % (gap_threshold*100), 'w')

    print('Number of sequences: %d' % total_sequences)
    print('Actin sequence length: %d' % length_sequence)
    print('\n')

    filtered_sequences = 0
    percent_gaps = np.zeros(total_sequences)

    for seq_num, record in enumerate(alignment):
        # Counts number of gaps in current sequence
        # Note: removes insertions via ungap method
        current_sequence = record.seq.ungap('.')
        temp_seq = Seq('')

        # Removes lowercase letters
        for residue in range(len(current_sequence)):
            if (current_sequence[residue].islower() == False):
                temp_seq = temp_seq + current_sequence[residue]

        current_sequence = temp_seq

        # Calculates % gaps in current sequence
        gap_count = current_sequence.count('-')
        percent_gaps[seq_num] = float(gap_count) / float(len(current_sequence))

        # Outputs current sequence that maintains minimum gap threshold
        if (percent_gaps[seq_num] <= gap_threshold):
            filtered_sequences += 1
            output_handle.write('>%s\n' % record.id +
                                ''.join(current_sequence) + '\n')

    removed_sequences = total_sequences - filtered_sequences

    print('Number of sequences removed: %d(%s%%)' % (
        removed_sequences, removed_sequences*100/total_sequences))
    print('Number of sequences kept: %d\n' % filtered_sequences)
    print('Wrote new file: \'' + output_handle.name + '\'\n')
    output_handle.close()
    msa_input.close()

    if (output_gaps == True):
        return percent_gaps


def main():
    """
    Main function that calls gap filter
    """

    # Adds a description for the help section
    parser = argparse.ArgumentParser(description='Filters sequences of a \
    Multiple-Sequence Alignment, given fraction of gaps (-) present.')

    parser.add_argument('msa_file', help='Multiple-Sequence Alignment file')
    parser.add_argument('gap_threshold', type=float, help='Gap threshold \
    (from 0 to 1.0) Default=0.25')
    parser.add_argument('-gf', action='store_true', help='Outputs a file \
    containing the fraction of gaps for each sequence. ')
    args = parser.parse_args()

    msa_input = args.msa_file
    gap_threshold = args.gap_threshold
    output_gap_fraction = args.gf

    # Gap filter function call
    p = gap_filter(open(msa_input), gap_threshold, output_gap_fraction)

    # Write gap fractions per sequence to a file
    if (output_gap_fraction == True):
        output_handle = 'gap_fraction_' + msa_input + '_f%dp' \
            % (gap_threshold*100)
        np.savetxt(output_handle, p, fmt='%.3f', newline='\n')
        print('Also wrote \'' + output_handle + '\'\n')

if __name__ == '__main__':
    main()
