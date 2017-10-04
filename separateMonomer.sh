#!/bin/bash
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#
#
#=======================================================#
# Written on March 24, 2016 
#=======================================================#
# By Kareem Mehrabiani
#                           
# MUST HAVE THE FOLLOWING FILES/SCRIPTS:
#
#   -reduce-2-mon.py (shrinks oligomers to single monomer)
#
#   -smog.contacts.CG (or similar SBM contact map)   
#
# GIVES YOU:
#          
#   -reduces oligomers to                                
#    monomers w/ chain #s
#
#   -interfacial contacts w/ chain #s
#    (as well as # of contacts)
#
#   -monomeric contacts
#    (as well as # of contacts)
#
#   -eternal life*
#
# OUTPUTS 3 FILES (unless you change this): 
#
#                      interfacial_pdb.contacts
#                      monomer_pdb.contacts
#                      pdb_full.contacts
#
#=======================================================#
# USAGE:  $: source separateMonomer.sh [cutoff value] 
#=======================================================#
#
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#
#       LOOK DOWN BELOW!!!!!!       #
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#

CONTACT_FILE=$1
C=$2   #cutoff

echo "Beginning initial setup..."
awk '{print $2,$4}' $CONTACT_FILE > protein_"$C"A.contacts
NEW_CONTACT_FILE=protein_"$C"A.contacts
#runs the reduce-2-mon.py script (NOTE: 'smog.contacts.CG' MUST be in the same folder, unless you change it.)
reduce-2-mon.py $NEW_CONTACT_FILE

#combines columns of file1 and file2, then prints them to a file called pdb.contacts
pr -m -t -s chains_"$C"A reduced_pdb_"$C"A.contacts | awk '{print $1,$3,$2,$4}' > pdb_full_"$C"A.contacts

#rm chains reduced_pdb.contacts

echo "Separating interfacial and monomer contacts from SBM file..."
#creates a file that contains only interfacial contacts from SBM
awk '{if ($1 != $3) {print $0}}' pdb_full_"$C"A.contacts > pdb_interfacial_"$C"A.contacts

#creates a file that contains only monomeric contacts from SBM
awk '{if ($1 == $3) {print $0}}' pdb_full_"$C"A.contacts > pdb_monomer_"$C"A.contacts 

echo " "
echo "# OF SBM INTERFACIAL CONTACTS:"
wc -l pdb_interfacial_"$C"A.contacts | awk '{print $1}'
echo "# OF SBM MONOMERIC CONTACTS:"
wc -l pdb_monomer_"$C"A.contacts | awk '{print $1}'

echo " "
echo "^^^^^^^^^^^^^^^^^"
echo "      done!      "
echo "^^^^^^^^^^^^^^^^^"
