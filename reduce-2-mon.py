#!/home/kmm5/anaconda2/bin/python
################################################################################
#   reduce-2-mon.py                                                            #
#   Author: Kareem Mehrabiani                                                  #
#   Created: June 6, 2016                                                      #
#                                                                              #
#   What does it do?                                                           #
#   Collapses homo-oligomeric protein contacts into a monomer so interfacial   #
#   contacts appear together with the monomer contacts.                        #
#                                                                              #
#   You need:                                                                  #
#           -a contact file                                                    #
#           -to know number of residues in a monomer (example: Monomeric       #
#            actin has 375 residues, but N*375 in an N-mer so use 375)         #
#                                                                              #
#   Usage: python reduce-2-mon.py [contact_file]                               #
#   NOTE: The [contact_file] must only contain pairs i and j. No Chains!       #
#                                                                              #
################################################################################

import numpy as np
import sys
import re

#/* INITIAL STUFF -------------------------------------------------------------

#Checks whether an input file was given (returns an error if False)
script_name = sys.argv[0]
if len(sys.argv) != 2:
    print "\nERROR: Please provide an input file after the script name."
    print "USAGE: %s [input_file]\n" % script_name
    exit(1)

filename = sys.argv[1]

#Imports contact_file and converts it into a numpy array
#Also checks if filename exists
try:
    contacts = np.loadtxt(filename, dtype=np.int32)
except IOError:
    print "File '%s' doesn't exist. Perhaps check spelling?\n" % filename
    exit(1)

#Extract number from filename for creating output filenames
regex = re.compile(r'\d+')
atom_res = regex.findall(filename)[0]
#print atom_res

#Number of residues in a monomer ***this may change if there are missing residues
#nres = 375     #actin
nres = 325      #mamk
#nres = 600     #hsp70

#/* PROCESSING THE ARRAY ------------------------------------------------------

#Calculates chain number by integer division
chains = np.divide(contacts-1, nres)
chain_filename = 'chains_' + atom_res + 'A'
np.savetxt(chain_filename, chains+1, fmt='%3i')

#Creates a place-holder array of zeros of size ( # of contacts, # of columns)
reduced_array = np.zeros((contacts.size/2,2))

#Returns the remainder based on the number of residues in a monomer
np.remainder(contacts, nres, reduced_array)
reduced_array[reduced_array==0] = nres

#Sorts reduced array so that the contacts appear (on a plot) on the top diagonal
sorted_array = np.sort(reduced_array)

#Saves the array to a file
main_outfile = 'reduced_pdb_' + atom_res + 'A.contacts'
np.savetxt(main_outfile, sorted_array, fmt='%3i')

print "\nCreated '%s' and '%s'\nEnjoy :)\n" % (chain_filename, main_outfile)
