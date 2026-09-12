#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=00:01:00
#SBATCH --job-name=slurm1

exec > slurm1.txt
cd $HOME/scratch
echo $PWD
echo $SLURM_JOB_NODELIST
echo $SLURM_NTASKS
