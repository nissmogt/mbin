#!/home/kmm5/anaconda2/bin/python
################################################################################
#   reduce-2-mon.py                                                            #
#   Author: Kareem Mehrabiani                                                  #
#   Created: June 6, 2016                                                      #
#   Edited: April 25, 2018                                                     #
#                                                                              #
#   What does it do?                                                           #
#   Collapses homo-oligomeric protein contacts into a monomer so interfacial   #
#   contacts appear together with the monomer contacts.                        #
#                                                                              #
#   Usage: python reduce-2-mon.py [contact_file] [length of monomer] [cutoff]  #
#   NOTE: The [contact_file] must only contain pairs i and j. No Chains!       #
#                                                                              #
################################################################################


## Reduce chain function definition ##
def reduce_chain(contact_map, nres, cutoff):
    import numpy as np

    #Calculates chain number by integer division
    contacts = np.loadtxt(contact_map, usecols=(1,3), dtype=np.int32)
    chains = np.divide(contacts-1, nres)
    chain_filename = 'chains_' + str(cutoff) + 'A'
    np.savetxt(chain_filename, chains+1, fmt='%3i')

    #Creates a place-holder array of zeros of size (# of contacts, # of columns)
    reduced_array = np.zeros((contacts.size/2,2))

    #Returns the remainder based on the number of residues in a monomer
    np.remainder(contacts, nres, reduced_array)
    reduced_array[reduced_array==0] = nres

    #Sort reduced array to appear (on a plot) on the top diagonal
    sorted_array = np.sort(reduced_array)

    #Saves the array to a file
    main_outfile = 'reduced_pdb_' + atom_res + 'A.contacts'
    np.savetxt(main_outfile, sorted_array, fmt='%3i')

    print "\nCreated '%s' and '%s'\nEnjoy :)\n" % (chain_filename, main_outfile)

## Main Script ##
def main():
    """
    Main function that calls reduce_chain().
    """

    import argparse

    parser = argparse.ArgumentParser(description="What do I do? Collapses\
        multichain protein pairs into one chain.")

    # Arguments
    parser.add_argument("contact_map", help="Column list of pairs.")
    parser.add_argument("length_monomer", type=int, help="Number of residues in\
            a monomer. Pay attention to missing residues.")
    parser.add_argument("cutoff", type=int, help="Cutoff used to make map.")
    args = parser.parse_args()

    contacts = args.contact_map 
    nres = args.length_monomer
    cutoff = args.cutoff

    reduce_chain(contacts, nres, cutoff)

if __name__=='__main__':
    main()

