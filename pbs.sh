#!/usr/bin/env bash
#PBS -q l_long
#PBS -m abe
#PBS -M pawel.ksieniewicz@pwr.edu.pl
#PBS -N ece
#PBS -l nodes=1:ppn=32
#PBS -l walltime=168:00:00

module add plgrid/tools/python/2.7.9
source ~/.python/bin/activate

cd ~/dev/eceExperiments
pip install -r requisites.txt

for datafile in ~/data/*
do
  ./experiment.py "$datafile" &
done

wait