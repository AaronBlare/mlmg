#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=1:00:00
#SBATCH --partition=gpu

printf "$1 \n\n"
printf "$2 \n\n"

cd $1

srun python -m $2
