import sys
import math
import random
import time
from subprocess import call, check_output

"""
Implements a uniform job benchmark for a SLURM cluster.

Team SLURM
Gerardo Ravago - gcravago@bu.edu
Ankit Sharma - ankitsh@bu.edu

"""

#Some cluster level configuration
cluster_size_nodes = 7
cpus_per_node = 2
cluster_size_cpus = cpus_per_node*cluster_size_nodes
sample_period = 5

class Slurm_job:
	def __init__(self, num_nodes, length, name):
		self.num_nodes = int(num_nodes)
		self.length = int(length)
		self.name = name
	
	def submit(self):
		minutes = int(self.length // 60)
		assert(minutes < 60)
		seconds = int(self.length % 60)
		#call("echo {:s}: Reserve {:d} nodes for {:d} seconds".format(self.name, self.num_nodes, self.length), shell=True)
		call("sbatch -t \"{:02d}:{:02d}\" -N {:d}  sleep.sh {:d}".format(minutes, seconds, self.num_nodes, self.length), shell=True)

	def run_time(self):
		return self.length * self.num_nodes / cluster_size_nodes

simple_job = Slurm_job(1, 30, 'Simple')
for i in range(0,140):
	simple_job.submit()

#Sample the remaining jobs until none remain
print('time_elapsed, jobs_remaining')
time_elapsed = 0
jobs_remaining = 230
while jobs_remaining is not 0:
	jobs_remaining = int(check_output('squeue | wc -l', shell=True)) - 1
	print('{:d},{:d}'.format(time_elapsed,jobs_remaining))
	time_elapsed += sample_period
	time.sleep(sample_period)

print("done.")