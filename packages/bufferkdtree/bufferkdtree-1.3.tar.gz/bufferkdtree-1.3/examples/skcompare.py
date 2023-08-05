#
# Copyright (C) 2013-2016 Fabian Gieseke <fabian.gieseke@di.ku.dk>
# License: GPL v2
#

"""
Nearest Neighbors (Scikit-Learn)
================================

Simple example comparing both CPU kd tree based 
implementations on a large-scale data set.
"""
print(__doc__)

import json
import time
import generate
from bufferkdtree.neighbors import NearestNeighbors
from sklearn.neighbors import NearestNeighbors as NearestNeighborsSKLEARN

# parameters
n_jobs = 4
leaf_size = 30
ofilename = "skcompare.json"
n_test_range = [100000, 250000, 500000, 750000, 1000000]
algorithms = ["kd_tree_sklearn", "kd_tree"]

verbose = 0
n_neighbors = 10

print("Parsing data ...")
Xtrain, Ytrain, Xtest = generate.get_data_set(NUM_TRAIN=2000000, NUM_TEST=10000000)
print("-------------------------------- DATA --------------------------------")
print("Number of training patterns:\t %i" % Xtrain.shape[0])
print("Number of test patterns:\t %i" % Xtest.shape[0])
print("Dimensionality of patterns:\t%i" % Xtrain.shape[1])
print("----------------------------------------------------------------------")

results = {}

def run_algorithm(n_test_local, leaf_size=30, algorithm="kd_tree"):

    print("----------------------------------------------------------------------")
    print("\n\nRunning %s for n_test=%i ...\n" % (algorithm, n_test_local))
    print("----------------------------------------------------------------------")

    Xtest_local = Xtest[:n_test_local, :]

    # instantiate model
    if algorithm == "kd_tree":
        nbrs = NearestNeighbors(n_neighbors=n_neighbors, 
                                algorithm=algorithm, 
                                n_jobs=n_jobs, 
                                leaf_size=leaf_size, 
                                verbose=verbose)
    else:
        nbrs = NearestNeighborsSKLEARN(n_neighbors=n_neighbors, 
                                       algorithm="kd_tree", 
                                       n_jobs=n_jobs, 
                                       leaf_size=leaf_size,                                        
                                       )
                
    # train model
    start_time = time.time()
    nbrs.fit(Xtrain)
    end_time = time.time()
    train_time = (end_time - start_time)
    print("Fitting time: %f" % train_time)

    # apply model (testing phase)
    start_time = time.time()
    _, _ = nbrs.kneighbors(Xtest_local)
    end_time = time.time()
    test_time = (end_time - start_time)
    print("Testing time: %f" % test_time)
    
    return train_time, test_time

for i in xrange(len(algorithms)):
    
    algorithm = algorithms[i]
    results[algorithm] = {}
    print("----------------------------------------------------------------------")
    print("\n\nRunning %s ...\n" % (algorithm))
    print("----------------------------------------------------------------------")
    for n_test in n_test_range:
        train_time, test_time = run_algorithm(n_test, 
                                              algorithm=algorithm, 
                                              leaf_size=leaf_size)
        results[algorithm][n_test] = {'train':train_time,
                                      'test':test_time,
                                      }

# write results after each step
print("Writing results to %s ..." % ofilename)
with open(ofilename, 'w') as f:
    json.dump(results, f)    
