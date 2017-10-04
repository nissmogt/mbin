#!/bin/bash

AATOM_DIR=$HOME/tools/smog203/templates/SBM_AA/
CA_DIR=$HOME/tools/smog203/templates/SBM_calpha+gaussian/
PDB=$1

smog2 -i $PDB -t $AATOM_DIR -tCG $CA_DIR
