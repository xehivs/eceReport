#!/bin/bash

pip install --upgrade -r requisites.txt

for datafile in data/*
do
  ./experiment.py "$datafile"
done
