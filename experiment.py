#!/usr/bin/env python
from ece import *
from ksskml import *

from pymongo import MongoClient
import sys

# Access DB
db = MongoClient("mongodb://156.17.43.89").ece.results

# Load dataset
datafile = sys.argv[1]
dbname = datafile.split('/')
dbname = dbname[len(dbname)-1]
#resampling = 500
#if len(sys.argv) > 2:
#	resampling = int(sys.argv[2])
dataset = Dataset(datafile)#, resampling)

# Parameters to test
radiuses = xrange(1,31,2)
grains = [15]
folds = xrange(0,5)
approaches = [ECEApproach.random]
limit = 15
votingMethods = [ExposerVotingMethod.lone, ExposerVotingMethod.theta1, ExposerVotingMethod.theta3, ExposerVotingMethod.thetas]

i = 0
amount = len(folds) * len(approaches) * len(votingMethods) * len(grains) * len(radiuses) 
print "%i instances to process" % amount

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
					    'dimensions': [ 2 ],
					    'eceApproach': approach,
					    'exposerVotingMethod': votingMethod
					}

					ensemble = ECE(dataset,configuration)
					ensemble.learn()
					ensemble.predict()
					scores = dataset.score()

					entry = {
						"dataset": dbname,
						"fold": fold,
					}

					entry.update(configuration)
					entry.update(scores)

					entry['eceApproach'] = entry['eceApproach'].value
					entry['exposerVotingMethod'] = entry['exposerVotingMethod'].value

					print "%02.2f %%\tF:%i / R:%.2f / G:%i / L:%i \t%.3f%%\t%s" % (100 * float(i) / amount, fold, fRadius, grain, limit,100*entry['accuracy'], dbname)
					i += 1

					db.insert_one(entry)

#cursor = db.find()
#for result in cursor:
#	print result
