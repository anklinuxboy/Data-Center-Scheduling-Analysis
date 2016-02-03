#!/bin/bash -x
for i in $(seq 0 6)
do
	echo "Setting up node0$i"
	scp slurm.conf ubuntu@node0${i}:~
	ssh ubuntu@node0${i} sudo cp slurm.conf /usr/local/etc/
	ssh ubuntu@node0${i} pkill slurmd*
	ssh ubuntu@node0${i} slurmd -c 
done

echo "Restart the control node"
sudo cp slurm.conf /usr/local/etc
pkill slurmctld*
slurmctld -c