#!/bin/bash

#mkdir -p rmsd
#for i in {0..9}
#    do
#        echo "0" "0" | g_rms -f ./run_$i/run_$i.xtc -s initial.gro -o ./rmsd/RMSD_$i
#        mv ./rmsd/RMSD_$i.xvg ./rmsd/RMSD_$i.txt
#    done

for i in {0..9}
    do
    for j in {11..19}
        do
            echo "0" "$j" | g_rms -f ./run_$i/run_$i.xtc -s initial.gro -n all.ndx -o ./rmsd/RMSD_$i$((j-10))
            mv ./rmsd/RMSD_$i$((j-10)).xvg ./rmsd/RMSD_$i$((j-10)).txt
        done
    done
