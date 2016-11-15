#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Skrypt ten odczytuje wszystkie pliki z wynikami z katalogu `results` i
# tworzy ich podsumowanie w katalogu `products`.

from os import listdir
from os.path import isfile, join
from operator import itemgetter
import csv

# Kontenery na podsumowania osiągów
bac = []
acc = []

# Wczytajmy wszystkie dane i wrzućmy je do kontenera `data`
data = []
directory = 'results'
files = [f for f in listdir(directory) if isfile(join(directory, f))]
for filename in files:
    with open('%s/%s' % (directory, filename), 'rb') as csvfile:
        records = list(csv.DictReader(csvfile))
        data.append({'filename': filename, 'records': records})

# Przetwarzanie pojedynczego pliku z wynikami (`unit`)
for unit in data:
    unitSummary = {}
    dbname = unit['filename'][2:-4]
    print "%s (db:%s)" % (unit['filename'], dbname)

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
            'accuracy': sum(float(d['accuracy']) for d in records) /
            len(records),
            'bac': sum(float(d['bac']) for d in records) / len(records),
            'radius': record['radius'],
            'grain': int(record['grain']),
            'limit': record['limit']
        }
        unitSummary[group] = summary

    # Wyłuskanie najlepszych wyników
    bestbac = sorted(
        unitSummary.values(),
        key=itemgetter('bac'))[-1].copy()
    bestacc = sorted(
        unitSummary.values(),
        key=itemgetter('accuracy'))[-1].copy()

    fnupdater = {'filename': dbname, 'experiment': unit['filename'][:1]}
    bestbac.update(fnupdater)
    bestacc.update(fnupdater)

    bac.append(bestbac)
    acc.append(bestacc)

    # Spłaszczenie i sortowanie wyniku
    unitSummary = sorted(unitSummary.values(), key=itemgetter(
        'radius', 'grain', 'limit'))

    # I zapis do pliku
    with open(('products/%s' % unit['filename']), 'wb') as csvfile:
        writer = csv.writer(
            csvfile,
            delimiter=',',
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL)
        writer.writerow(unitSummary[0].keys())
        # Nagłówki
        for row in unitSummary:
            writer.writerow(row.values())

# Podsumowanie wielu eksperymentów
accSummary = {}
bacSummary = {}

for item in acc:
    key = item['filename']
    if key not in accSummary:
        accSummary.update({key: []})
    accSummary[key].append(item.copy())

for item in bac:
    key = item['filename']
    if key not in bacSummary:
        bacSummary.update({key: []})
    bacSummary[key].append(item.copy())

for item in accSummary:
    newcomer = {}
    for record in accSummary[item]:
        exp = record['experiment']
        for key in ['accuracy', 'bac', 'limit', 'radius', 'grain']:
            record['%s%s' % (key, exp)] = record.pop(key)
        newcomer.update(record)
    accSummary[item] = newcomer

for item in bacSummary:
    newcomer = {}
    for record in bacSummary[item]:
        exp = record['experiment']
        for key in ['accuracy', 'bac', 'limit', 'radius', 'grain']:
            record['%s%s' % (key, exp)] = record.pop(key)
        newcomer.update(record)
    bacSummary[item] = newcomer


# Zapis podsumowań
with open('products/bac.csv', 'wb') as bacfile:
    bacwriter = csv.writer(
        bacfile,
        delimiter=',',
        quotechar='"',
        quoting=csv.QUOTE_MINIMAL)
    with open('products/acc.csv', 'wb') as accfile:
        accwriter = csv.writer(
            accfile,
            delimiter=',',
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL)

        # Nagłówki
        bacwriter.writerow(bacSummary.values()[0].keys())
        accwriter.writerow(accSummary.values()[0].keys())
        for row in bacSummary.values():
            bacwriter.writerow(row.values())
        for row in accSummary.values():
            accwriter.writerow(row.values())
