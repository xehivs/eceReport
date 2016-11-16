#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ece import *
from ksskml import *

import sys
import csv

# Load dataset
datafile = sys.argv[1]
dbname = datafile.split('/')
dbname = dbname[len(dbname) - 1]
resampling = 200
if len(sys.argv) > 2:
    resampling = int(sys.argv[2])
dataset = Dataset(datafile)


# Parametry eksperymentów
parameters = {
    'heart': {
        'radius': 21,
        'grain': 5
    },
    'hayes': {
        'radius': 3,
        'grain': 7
    },
    'soybean': {
        'radius': 9,
        'grain': 19
    },
    'iris': {
        'radius': 15,
        'grain': 3
    },
    'german': {
        'radius': 5,
        'grain': 15
    },
    'ionosphere': {
        'radius': 1,
        'grain': 17
    },
    'australian': {
        'radius': 25,
        'grain': 5
    },
    'balance': {
        'radius': 1,
        'grain': 17
    },
    'breastcan': {
        'radius': 19,
        'grain': 19
    },
    'diabetes': {
        'radius': 23,
        'grain': 13
    }
}

# Parameters to test
dbn = dbname[:-4]

radiuses = [parameters[dbn]['radius']]
grains = [parameters[dbn]['grain']]
folds = xrange(0, 5)
approaches = [ECEApproach.random]
limits = xrange(1, 20, 2)
votingMethods = [ExposerVotingMethod.lone]
i = 0
amount = len(folds) * len(approaches) * \
    len(votingMethods) * len(grains) * len(radiuses) * len(limits)
print "\t%i instances to process" % amount

with open('results/l_%s' % dbname, 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    headers = ['fold', 'radius', 'grain', 'limit', 'accuracy', 'bac']
    writer.writerow(headers)
    for fold in folds:
        dataset.setCV(fold)
        for approach in approaches:
            for limit in limits:
                for votingMethod in votingMethods:
                    for grain in grains:
                        for radius in radiuses:
                            dataset.clearSupports()

                            fRadius = radius / 100.

                            configuration = {
                                'radius': radius,
                                'grain': grain,
                                'limit': limit,
                                'dimensions': [2],
                                'eceApproach': approach,
                                'exposerVotingMethod': votingMethod
                            }

                            ensemble = ECE(dataset, configuration)
                            ensemble.learn()
                            ensemble.predict()
                            scores = dataset.score()

                            entry = {
                                "dataset": dbname,
                                "fold": fold,
                            }

                            entry.update(configuration)
                            entry.update(scores)

                            row = [fold, fRadius, grain, limit,
                                entry['accuracy'], entry['bac']]
                            print row
                            writer.writerow(row)
                            i += 1
