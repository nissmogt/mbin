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
#   -filter_monomer.cpp (separates DCA contacts by mon/dimer)
#
#   -smog.contacts.CG (or similar SBM contact map)   
#   -DCA contact map (should only be 2 columns)
#   -monomer_pdb.contacts (or similar SBM contact map)
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
#   -monomer and dimer DCA contacts
#
#   -eternal life*
#
# OUTPUTS FOUR FILES (unless you change this): 
#
#                      interfacial_pdb.contacts
#                      monomer_pdb.contacts
#                      pdb_full.contacts
#                      monomer_DCA.contacts
#                      dimer_DCA.contacts                      
#
#=======================================================#
# USAGE:  $: source magic.sh
#=======================================================#
#
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#
#       LOOK DOWN BELOW!!!!!!       #
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#

echo "Beginning initial setup..."
#runs the reduce-2-mon.py script (NOTE: 'smog.contacts.CG' MUST be in the same folder, unless you change it.)
reduce-2-mon.py sbm/smog8A.contacts.cg

#combines columns of file1 and file2, then prints them to a file called pdb.contacts
#pr -m -t -s chains_12A reduced_pdb_12A.contacts | awk '{print $1,$3,$2,$4}' > pdb_full_12A.contacts
pr -m -t -s chains_8A reduced_pdb_8A.contacts | awk '{print $1,$3,$2,$4}' > pdb_full_8A.contacts

#rm chains reduced_pdb.contacts

echo "Separating interfacial and monomer contacts from SBM file..."
#creates a file that contains only interfacial contacts from SBM
awk '{if ($1 != $3) {print $0}}' pdb_full_12A.contacts > pdb_interfacial_12A.contacts

#creates a file that contains only monomeric contacts from SBM
awk '{if ($1 == $3) {print $0}}' pdb_full_12A.contacts > pdb_monomer_12A.contacts 

#runs c++ script that separates DCA contacts by monomer and dimer contacts (change files that match with your filenames)
echo "Filtering out monomer contacts from DCA..."
g++ filter_monomer.cpp
a.out
rm a.out

echo " "
echo "# OF SBM INTERFACIAL CONTACTS:"
wc -l pdb_interfacial_12A.contacts | awk '{print $1}'
echo "# OF SBM MONOMERIC CONTACTS:"
wc -l pdb_monomer_12A.contacts | awk '{print $1}'

echo "Preparing DCA interfacial contacts for top file..."
echo "Total # of DCA contacts in the 9mer:"
wc -l dca_9mer.contacts
#wc -l dca_9mer_sasa.contacts
#prepare dimer contacts for input into top file
#awk '{printf "%.0f %.0f %.0f %.2f %.2f %.2f %10.9e\n", $1,$2,$3=6,$4=5,$5=0.8,$6=0.05,$7=1.677721600e-05}' dca_9mer_sasa.contacts > rdy4top_dimer_sasa.contacts
awk '{printf "%.0f %.0f %.0f %.2f %.2f %.2f %10.9e\n", $1,$2,$3=6,$4=5,$5=0.8,$6=0.05,$7=1.677721600e-05}' dca_9mer.contacts > rdy4top_dimer.contacts
awk '{print $1,$2}' dca_9mer.contacts > rdy4top_exclusion.contacts

echo " "
echo "^^^^^^^^^^^^^^^^^^^^^^^^^^"
echo "      Magic is done!      "
echo "^^^^^^^^^^^^^^^^^^^^^^^^^^"
