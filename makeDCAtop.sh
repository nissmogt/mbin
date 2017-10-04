#!/bin/bash
#
#====================================================================#
#   Script Name: makeDCAtop.sh
#   Author: Kareem Mehrabiani
#   Written on 10 August 2017 
#====================================================================#
#   Usage: makeDCAtop.sh
#   Output: DCA contacts with gaussian potential parameters
#           and exclusion list which are the DCA contacts.
#====================================================================#

echo "Making symmetric DCA interfacial contacts for each chain..."
symmetrize_pairs.py

echo "Total number of DCA contacts in the N-mer:"
wc -l DCAsym.contacts

# Appending Gaussian potential parameters to DCA (i,j) pairs
awk '{printf "%.0f %.0f %.0f %.2f %.2f %.2f %10.9e\n", $1,$2,$3=6,$4=5,$5=1.2,
     $6=1.0,$7=1.677721600e-05}' DCAsym.contacts > dca4top.contacts

awk '{print $1,$2}' DCAsym.contacts > dca4top_exclusion.contacts

echo " "
echo "^^^^^^^^^^^^^^^^^^^^^^^^^^"
echo "^^^^^^^^^^^^^^^^^^^^^^^^^^"
