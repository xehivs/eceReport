#!/usr/bin/env python
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

print "DB: %s" % dataset

# Parameters to test
radiuses = xrange(1, 31, 2)
grains = [15]
folds = xrange(0, 5)
approaches = [ECEApproach.random]
limit = 15
votingMethods = [ExposerVotingMethod.lone]

i = 0
amount = len(folds) * len(approaches) * \
    len(votingMethods) * len(grains) * len(radiuses)
print "\t%i instances to process" % amount

with open('results/r_%s' % dbname, 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    headers = ['fold', 'radius', 'grain', 'limit', 'accuracy', 'bac']
    writer.writerow(headers)
    for fold in folds:
        dataset.setCV(fold)
        for approach in approaches:
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
