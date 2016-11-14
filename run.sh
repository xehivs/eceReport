#!/bin/bash
DATAFILES=./data/*

for f in $DATAFILES
do
  echo "Processing $f file..."
  ./experiment.py $f
done
