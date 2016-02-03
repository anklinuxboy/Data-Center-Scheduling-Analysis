#!/bin/bash

cd parsec-3.0
source env.sh
parsecmgmt -a run -p $1 -i native -n 2
