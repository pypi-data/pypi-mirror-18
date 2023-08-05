#
# Copyright (C) 2013-2016 Fabian Gieseke <fabian.gieseke@di.ku.dk>
# License: GPL v2
#

"""
Nearest Neighbors and Artificial Data
=====================================

This example demonstrates the use of the different 
implementations given on a small artifical data set.

Note: The platform and the device needs to be specified below 
(via the parameter 'plat_dev_ids').
"""
print(__doc__)

import numpy
from bufferkdtree import NearestNeighbors

n_neighbors = 10
plat_dev_ids = {0:[0]}
n_jobs = 1
verbose = 1

X = numpy.random.uniform(low=-1, high=1, size=(10000,10))

# (1) apply buffer k-d tree implementation
nbrs_buffer_kd_tree = NearestNeighbors(algorithm="buffer_kd_tree", 
                        tree_depth=9, 
                        plat_dev_ids=plat_dev_ids, 
                        verbose=verbose)    
nbrs_buffer_kd_tree.fit(X)
dists, inds = nbrs_buffer_kd_tree.kneighbors(X, n_neighbors=n_neighbors)
print("\nbuffer_kd_tree output\n" + str(dists[0]))

# (2) apply brute-force implementation
nbrs_brute = NearestNeighbors(algorithm="brute", 
                        plat_dev_ids=plat_dev_ids, 
                        verbose=verbose)    
nbrs_brute.fit(X)
dists, inds = nbrs_brute.kneighbors(X, n_neighbors=n_neighbors)
print("\nbrute output\n" + str(dists[0]))

# (3) apply k-d tree mplementation
nbrs_kd_tree = NearestNeighbors(algorithm="kd_tree", 
                        n_jobs=n_jobs, 
                        verbose=verbose)    
nbrs_kd_tree.fit(X)
dists, inds = nbrs_kd_tree.kneighbors(X, n_neighbors=n_neighbors)
print("\nkd_tree output\n" + str(dists[0]) + "\n")
