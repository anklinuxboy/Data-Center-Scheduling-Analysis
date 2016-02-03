#!/bin/bash -x

for node in node{0..6}
do
	echo "Transferring $1 to $node"
	scp $1 ubuntu@$node:~
done