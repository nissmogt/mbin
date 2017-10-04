#!/bin/bash

#Inputs: old_top_8A.pairs, full_top_8A.pairs
#Output: top.chain, sbm_full_top.pairs, old_top_monomer.pairs, old_top_inter.pairs, new_top_nointer.pairs
#        new_top_inter.pairs

# Input file
old_pairs=$1

# Calls python script which calculates chain numbers from residue pairs
xtract-chain-top.py $old_pairs

# Appends chain number to given pairs to corresponding column number
pr -m -t -s chains.top $old_pairs > full_top.pairs

# Separates pairs by interfacial and monomeric pairs
awk '{if ($1 == $2) {print $3,$4,$5,$6,$7,$8,$9}}' full_top.pairs > pairs_monomer_8A.top
awk '{if ($1 != $2) {print $3,$4,$5,$6,$7,$8,$9}}' full_top.pairs > pairs_inter_8A.top

# Exclusion pairs are just the i,j pairs
awk '{print $1, $2}' pairs_monomer_8A.top > exclusion_mon_8A.top
awk '{print $1, $2}' pairs_inter_8A.top > exclusion_inter_8A.top

#removes the interfacial contacts from 'pairs.top'
#awk 'NR==FNR {a[$1,$2];next} ($3,$4) in a' top_monomer_8A.pairs full_top_8A.pairs > new_top_monomer_8A.pairs
#awk 'NR==FNR {a[$1,$2];next} ($3,$4) in a' top_inter_8A.pairs full_top_8A.pairs > new_top_inter_8A.pairs

rm full_top.pairs
