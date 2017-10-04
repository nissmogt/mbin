#!/bin/bash

DCA_PAIRS=$1
for i in {100..1000..100} 
do
    head -n $i $DCA_PAIRS > top$i
done

head -n 2000 $DCA_PAIRS > top2000
