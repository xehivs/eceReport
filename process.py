#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Skrypt ten odczytuje wszystkie pliki z wynikami z katalogu `results` i
# tworzy ich podsumowanie w katalogu `products`.

from os import listdir
from os.path import isfile, join
from operator import itemgetter
import csv

# Wczytajmy wszystkie dane i wrzućmy je do kontenera `data`
data = []

directory = 'results'
files = [f for f in listdir(directory) if isfile(join(directory, f))]
for filename in files:
    with open('%s/%s' % (directory, filename), 'rb') as csvfile:
        records = list(csv.DictReader(csvfile))
        data.append({'filename': filename, 'records': records})

# Przetwarzanie pojedynczego pliku z wynikami (`unit`)
unit = data[0]
unitSummary = {}
print unit['filename']

# Grupowanie po unikalnych kombinacjach parametrów
for record in unit['records']:
    key = ('r%sg%sl%s' % (
        record['radius'],
        record['grain'],
        record['limit']
        ))
    if key not in unitSummary:
        unitSummary.update({key: []})
    unitSummary[key].append(record)

# Podsumowanie grup
for group in unitSummary:
    records = unitSummary[group]
    record = records[0]
    summary = {
        'accuracy': sum(float(d['accuracy']) for d in records) / len(records),
        'bac': sum(float(d['bac']) for d in records) / len(records),
        'radius': record['radius'],
        'grain': record['grain'],
        'limit': record['limit']
    }
    unitSummary[group] = summary

# Spłaszczenie i sortowanie wyniku
unitSummary = sorted(unitSummary.values(), key=itemgetter(
    'radius', 'grain', 'limit'))
print unitSummary
