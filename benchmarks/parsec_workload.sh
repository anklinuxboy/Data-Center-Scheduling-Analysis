#!/bin/bash

for i in $(seq 1 250)
do
	sbatch -t "02:00" parsec.sh blackscholes
	sbatch -t "04:00" parsec.sh streamcluster
	sbatch -t "02:00" parsec.sh canneal
	sbatch -t "04:00" parsec.sh facesim
done

for i in $(seq 0 20 3600)
do
	sleep 20
	echo "$i,$[$(squeue | wc -l)-1]" 
done