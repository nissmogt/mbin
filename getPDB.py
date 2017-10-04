#!/home/kmm5/anaconda2/bin/python
#
#==============================================================================
#   getPDB.py
#   Author: Kareem Mehrabiani
#   Written: June 6, 2016
#
#   What does it do?
#       It downloads pdb file(s) specified by your input(s).
#
#   Usage: ./getPDB.py [PDB_ID_1] [PDB_ID_2] ... [PDB_ID_N] or PDB list in 
#          text file.
#
#   Outputs: 'PDB_ID_1.pdb' ... 'PDB_ID_N.pdb'
#
#==============================================================================

import sys
import os
import re
import urllib as ul
import numpy as np


script_name = sys.argv[0]
#Checks whether input(s) was given (returns an error if False)
if len(sys.argv) < 2:
    print "\nERROR: Provide at least one PDB Id or a textfile of Id's."
    print "USAGE: %s [PDB_ID_1]...[PDB_ID_N] or PDB_ID_list.txt\n" % script_name
    exit(1)

if os.path.isfile(sys.argv[1]) == True:
    pdb = np.genfromtxt(sys.argv[1], dtype='str')
    if pdb.size <  2:
        print "\nERROR: Check your PDB list file (it may not be formatted correctly)."
        print "       Or you may have one PDB ID in your list file (if this is the"
        print "       case, don't even use a list file!\n"
        print "USAGE: %s [PDB_ID_1]...[PDB_ID_N] or PDB_ID_list.txt\n" % script_name
        exit(1)
    number_ids = pdb.size

else:
    pdb = sys.argv[1:]
    number_ids = len(pdb)

for ids in pdb:

    #Gets the PDB_ID(s) from input(s) or file
    regex = re.compile(r'\w{4}')
    pdb_id = regex.findall(ids)[0]
    print "Downloading " + pdb_id + "..." 

    #Retrieves PDB info from the web
    url = "http://files.rcsb.org/view/" + pdb_id + ".pdb" 
    destination_filename = pdb_id + ".pdb"

    #Saves PDB info to a file
    ul.urlretrieve(url, destination_filename)

print "Congratulations, you won!\n"
