#!/bin/bash
###############################################################################
# script name: rank_dca.sh
# Author: Kareem Mehrabiani
# Date  : 23rd April 2017
#
# Description: Ranks the couplings outputed by plmDCA by FN score. The
#              couplings which have sequence distance < 4 are filtered out.
#
# Input: You need a contact file that includes the coupling pairs and FN score.
#
# Output: A ranked contact file where the distance btwn pair i & j > 4 residues.
#
# Usage: $./rank_dca.sh [contact_file]
#
###############################################################################

CONTACT_FILE=$1

awk -F, '{print $1,$2,$3}' $CONTACT_FILE | awk '$2-$1>5' | 

sort -k3gr > "ranked.fn"
