import sys
import math
import random
import time
from subprocess import call, check_output

"""
Implements the ESP-2 benchmark for a SLURM cluster.

Team SLURM
Gerardo Ravago - gcravago@bu.edu
Ankit Sharma - ankitsh@bu.edu

"""

random.seed('EC700 Is Awesome')

#Some cluster level configuration
cluster_size_nodes = 7
cpus_per_node = 2
cluster_size_cpus = cpus_per_node*cluster_size_nodes
sample_period = 5

#Use this constant to scale down the run time of ESP. The original benchmark has an ideal runtime of ~3 hours
#Scaling down by 18 results in SLURM reiring all jobs in about 3 hours
scale_factor = 1.0/18

# Initial values for ESP-2 benchmarks taken from paper
# d = job concurrency relative to system
# k = job instances
# pi = target runtime
esp2_initial_values = {
	'A' : {
		'd' : 0.03125,
		'k' : 75,
		'pi' : 267
	},
	'B' : {
		'd' : 0.06250,
		'k' : 9,
		'pi' : 322
	},
	'C' : {
		'd' : 0.50000,
		'k' : 3,
		'pi' : 534
	},
	'D' : {
		'd' : 0.25000,
		'k' : 3,
		'pi' : 616
	},
	'E' : {
		'd' : 0.50000,
		'k' : 3,
		'pi' : 315
	},
	'F' : {
		'd' : 0.06250,
		'k' : 9,
		'pi' : 1846
	},
	'G' : {
		'd' : 0.12500,
		'k' : 6,
		'pi' : 1334
	},
	'H' : {
		'd' : 0.15820,
		'k' : 6,
		'pi' : 1067
	},
	'I' : {
		'd' : 0.03125,
		'k' : 24,
		'pi' : 1432
	},
	'J' : {
		'd' : 0.06250,
		'k' : 24,
		'pi' : 725
	},
	'K' : {
		'd' : 0.09570,
		'k' : 15,
		'pi' : 487
	},
	'L' : {
		'd' : 0.12500,
		'k' : 36,
		'pi' : 366
	},
	'M' : {
		'd' : 0.25000,
		'k' : 15,
		'pi' : 187
	}
	# Z Tests are not submitted in random order
	# 'Z' : {
	# 	'd' : 1.00000,
	# 	'k' : 2,
	# 	'pi' : 100
	# }
}

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

#Create a list of all the SLURM jobs to pick from
work_sk = 0
job_queue = []
for job_type in esp2_initial_values:
	job = esp2_initial_values[job_type]

	run_time = math.ceil(job['pi']*scale_factor)
	work_sk += cluster_size_cpus * job['d'] * job['k'] * run_time

	num_nodes = math.ceil(job['d']*cluster_size_nodes)
	assert(num_nodes<=cluster_size_nodes)
	#Create the job queue here
	for i in range(0,job['k']):
		job_queue.append(Slurm_job(num_nodes, run_time, job_type))
t_best = work_sk/cluster_size_cpus
print("Theoretical Best Running Time {:.2f}s".format(t_best))

#Submit the jobs in random order
#Z Tests must be scheduled after 10% and 90% of the ideal time
z_test = Slurm_job(cluster_size_nodes, math.ceil(100*scale_factor), 'Z')
t_ideal = 0
z1_submit = t_best * 0.1
z2_submit = t_best * 0.9
z1_done = False
z2_done = False
while len(job_queue) is not 0:
	job = random.choice(job_queue)
	job_queue.remove(job)
	job.submit()
	t_ideal += job.run_time()
	if t_ideal > z1_submit and not z1_done:
		z_test.submit()
		z1_done = True
	if t_ideal > z2_submit and not z2_done:
		z_test.submit()
		z2_done = True
print('Submitted all 230 Jobs')


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