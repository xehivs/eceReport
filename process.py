#!/usr/bin/env python
from os import listdir
from os.path import isfile, join
import csv

files = [f for f in listdir('results') if isfile(join('results', f))]

for file in files:
    print file
print 'Ciul'
