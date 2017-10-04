#!/home/kmm5/anaconda2/bin/python
################################################################################
#   xtract-chain-top.py                                                        #
#   Author: Kareem Mehrabiani                                                  #
#   Created: June 6, 2016                                                      #
#                                                                              #
#   What does it do?                                                           #
#       Extracts chain numbers from contact files given an N residue protein.  #
#                                                                              #
#   You need:                                                                  #
#           -[pairs] entries file from topfile                                 #
#           -to know number of residues in a monomer (example: Monomeric       #
#            actin has 375 residues, but N*375 in an N-mer so use 375)         #
#                                                                              #
#   Usage: python xtract-chain-top.py [pairs-file]                             #
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
    contacts = np.loadtxt(filename, usecols=(0,1), dtype=np.int32)
except IOError:
    print "File '%s' doesn't exist. Perhaps check spelling?\n" % filename
    exit(1)

#Number of residues in a monomer (will vary depending on protein)
nres = 375

#/* PROCESSING THE ARRAY ------------------------------------------------------

#Calculates chain number by integer division
chains = np.divide(contacts-1, nres)
np.savetxt('chains.top', chains+1, fmt='%3i')
