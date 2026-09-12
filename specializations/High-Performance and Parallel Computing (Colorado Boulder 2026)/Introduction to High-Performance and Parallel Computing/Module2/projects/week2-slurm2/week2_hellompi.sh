#!/bin/bash
#SBATCH --nodes=4
#SBATCH --time=00:00:30

exec > week2_hellompi.txt
module purge
module load mpich
mpif90 hello_new.f90 -o hello_new
mpirun -np 4 ./hello_new

