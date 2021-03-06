## EC700 Final Project
### Job Throughput Analysis of Data Center Scheduling Algorithms
This project was undertaken as the final project for EC700 Advanced Computing Systems and Architecture at Boston University College of Engineering taught by [Dr. Ayse Coskun](http://www.bu.edu/eng/profile/ayse-coskun)

[SLURM](http://slurm.schedmd.com) ( Simple Linux Utility for Resource Management) is a workload manager being used by 60% of the TOP500 supercomputers. [SLURM Wiki](https://en.wikipedia.org/wiki/Slurm_Workload_Manager)

#### Team SLURM
**Gerardo Ravago** - gcravago@bu.edu
**Ankit Sharma** - ankitsh@bu.edu

#### Manifest:
#### /README
--------------
```
/slurm_setup/update_daemons.sh - Deploys a slurm.conf file and restarts all SLURM daemons
/slurm_setup/transfer.sh - SCP's a file to all the SLURM nodes
/slurm_setup/slurm.conf - Example slurm.conf file for our cluster
/slurm_setup/setup.sh - Installs and sets up all of the pre-requisites for a new instance
/benchmarks/uniform_workload.py - Uniform workload benchmark, schedules an hour's worth of single node jobs with the same execution time.
/benchmarks/sleep.sh - Bash wrapper script to sleep for n seconds
/benchmarks/parsec_workload.sh - Schedules our PARSEC based workload
/benchmarks/parsec.sh - Bash wrapper script to schedule to run a specified PARSEC benchmark
/benchmarks/esp_workload.py - Our scaled down version of the Effective System Performance (ESP) benchmark
```
#### Setup Instructions:
------------------------
```
1. Setup a cluster of 8 Ubuntu-14.04LTS-amd64 instances with the m1.2core flavor on Massachusettes Open Cloud.
  - Be sure to setup and install your ssh keypair as well.
  - Name one of the instances slurm-primary and the others node00-node06

2. For convenience, take note of the IP addresses assigned to each instance.
  - Stash them in a text file called hosts in /etc/hosts file format
  	127.0.0.1		example.com
  - Cat the file into your own /etc/hosts file

3. Create a Munge Key for your cluster
  - dd if=/dev/urandom bs=1 count=1024 > munge.key

4. The included slurm_setup/transfer.sh script can be used to quickly SCP a file to the home directory of all your nodes
  - SCP hosts, munge.key, and the included slurm_setup/setup.sh files to all the nodes

5. Run the setup.sh file on all the nodes.
  - This takes care of most of the setup for SLURM, MUNGE, and PARSEC for you
  - It will require some attention, just say yes to everything and read nothing :)
  - For the mail server setup select local

6. Sync up the public keys.
  - Write a quick script to grab all the public keys that were just generated and concatenate them into the same file.
  - cat this file into the authorized_keys file of slurm-primary
  - Write another script to cat slurm-primary's public key into the authorized_keys file of all the compute nodes

7. Sync up the time on all servers
  - A simple way to do this is to run the following command on each compute node.
  - sudo date --set="$(ssh ubuntu@slurm-primary date)"

8. Create and deploy a slurm.conf file
  - Update the IP addresses in included slurm.conf using your hosts file
  - Save it to slurm-primary's home directory and run the included update_daemons.sh script to deploy it
  - SLURM should now be up and running if these instructions are correct.

9. Test SLURM
  - sinfo should indicate that all nodes are connected and idle
  - srun echo "hello" should schedule echo on a node and redirect it to your stdout
```

#### Running the Benchmarks:
-----------------------------
```
1. Edit your slurm.conf for the setting that you would like to evaluate.
2. Deploy your configuration using the update_daemons.sh file
3. Run the respective workload script inside the benchmarks folder.
4. Results will print to the stdout.
```
The PDF included is an IEEE format research paper detailing our Analysis.
