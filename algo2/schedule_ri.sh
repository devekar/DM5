#!/bin/bash

for sup in 7 8 9 10
do
	for conf in 60 65 70 75 80 85 90
	do
	    for clusters in 8 16
	    do
		    outfile=RESULTS/CBA_${sup}_${conf}_${clusters}.output
		    command="sbatch -N 1 --output=$outfile ./ri_run.sbatch ${sup} ${conf} ${clusters}"
		    echo $command
		    `$command`
        done
	done
done

