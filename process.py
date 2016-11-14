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
    unit['filename'] = unit['filename'][2:-4]
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
            'accuracy': sum(float(d['accuracy']) for d in records) /
            len(records),
            'bac': sum(float(d['bac']) for d in records) / len(records),
            'radius': record['radius'],
            'grain': record['grain'],
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

    fnupdater = {'filename': unit['filename']}
    bestbac.update(fnupdater)
    bestacc.update(fnupdater)

    print fnupdater

    bac.append(bestbac)
    acc.append(bestacc)

    print bestbac

    # Spłaszczenie i sortowanie wyniku
    unitSummary = sorted(unitSummary.values(), key=itemgetter(
        'radius', 'grain', 'limit'))

    # I zapis do pliku
    with open(('products/%s.csv' % unit['filename']), 'wb') as csvfile:
        writer = csv.writer(
            csvfile,
            delimiter=',',
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL)
        writer.writerow(unitSummary[0].keys())
        # Nagłówki
        for row in unitSummary:
            writer.writerow(row.values())

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
        bacwriter.writerow(bac[0].keys())
        accwriter.writerow(acc[0].keys())
        for row in bac:
            bacwriter.writerow(row.values())
        for row in acc:
            accwriter.writerow(row.values())
