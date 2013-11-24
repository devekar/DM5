#!/bin/bash
# Job name:
#SBATCH --job-name=DM

# use --exclusive to get the whole nodes exclusively for this job
#SBATCH --exclusive

#SBATCH --time=08:00:00

#SBATCH -p batch

# Set up work environment
#. /opt/intel/mkl/bin/mklvars.sh intel64

# Set up your environment 
#
# Start
s=$1
c=$2
python CBA.py tm_train.csv tm_test.csv -s${s}m3 -c${c}
