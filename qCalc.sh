energySelection=7

startTime=10
endTime=5000

for i in {0..9}
#for T in 120
do
    (

    cd ./run_$i
    rm qval_$i.out
    g_kuh_h -abscut -noshortcut -cut 0.1 -f run_$i.xtc -s run.tpr -n ../index.ndx -o qval_$i.out
    #g_kuh_h -b $startTime -e $endTime -abscut -noshortcut -cut 0.1 -f run_$i.xtc -s run.tpr -n ../index.ndx -o qval_$i.out
    #echo $energySelection | g_energy_h -b $startTime -e $endTime -f run_$i.edr -s run.tpr -o energy_pe.xvg;
    #tail -n+20 energy_pe.xvg >> list_energy_pe.txt;

    )

done
