#!/bin/bash

for sup in 0.5 1 1.5 2 2.5 3 3.5 4
do
	for conf in 60 65 70 75 80 85 90
	do
		outfile=RESULTS/CBA_${sup}_${conf}.output
		command="sbatch -N 1 --output=$outfile ./ri_run.sbatch ${sup} ${conf}"
		echo $command
		`$command`
	done
done

