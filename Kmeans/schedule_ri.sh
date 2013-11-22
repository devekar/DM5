#!/bin/bash

for clusters in 8 16 32 64
do
	outfile=RESULTS/Kmeans_${clusters}.output
	command="sbatch -N 1 --output=$outfile ./ri_run.sbatch ${clusters}"
	echo $command
	`$command`
done

