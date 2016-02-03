#!/bin/bash -x
echo "Hack for infinite Bash history"
export HISTSIZE=""

echo "Update Ubuntu and install pre-requisites"
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install git build-essential munge libmunge-dev mailutils

echo "Install SLURM"
git clone https://github.com/SchedMD/slurm.git
cd slurm
git checkout slurm-15-08-4-1
./configure
make
sudo make install
ldconfig -nv /usr/local/lib/

echo "Install Munge"
cd
sudo cp munge.key /etc/munge/
sudo chown munge /etc/munge/munge.key
sudo chmod 400 /etc/munge/munge.key
sudo chmod g-w /var/log/

echo "Install PARSEC"
cd
wget http://parsec.cs.princeton.edu/download/3.0/parsec-3.0-core.tar.gz
tar -xvzf parsec-3.0-core.tar.gz
wget http://parsec.cs.princeton.edu/download/3.0/parsec-3.0-input-native.tar.gz
tar -xvzf parsec-3.0-input-native.tar.gz
cd parsec-3.0
source env.sh
for bench in {blackscholes,facesim,canneal,streamcluster}
do
	parsecmgmt -a build -p ${bench}
done

echo "Generate Public Key"
ssh-keygen