from __future__ import division
from operator import itemgetter
import sys
import math
import itertools


def convert_TM_to_DM(tm):
    dm = [ [0]*1156 for i in xrange(len(tm)) ]

    for row_idx in xrange(len(tm)):
        for idx in tm[row_idx]:
            dm[row_idx][idx] = 1

    return dm


def get_mean(vector):
    return sum(vector) / len(vector)


def get_cluster_mean_vector(list):
    return map(get_mean, zip(*list))


def get_representative_means(tm):
    dm = convert_TM_to_DM(tm)
    vector = get_cluster_mean_vector(dm)

    return vector


'''Compute magnitude of a vector'''
def magnitude(vector):
    mag = 0;
    for item in vector:
        mag += item * item
    return math.sqrt(mag)


'''Compute cosine distance between two numeric vectors'''
def cosine_dist(vector1, vector2):
    dot_product = 0;
    for i1, i2 in itertools.izip(vector1, vector2):
        dot_product += i1 * i2;

    mag1 = magnitude(vector1);
    mag2 = magnitude(vector2);
    cosine_sim = dot_product / (mag1 * mag2)
    return 1 - cosine_sim 


# Return clusters, where each cluster consists of test instances that belong to that cluster(identified by index)
def cluster_test_set(test_features_list, test_labels_list, cluster_means):
    test_features_clusters = [ [] for i in range(len(cluster_means)) ]
    test_labels_clusters =   [ [] for i in range(len(cluster_means)) ]

    test_dm = convert_TM_to_DM(test_features_list)
    for idx, feature_vector in enumerate(test_dm):
        distances = []
        for mean_vector in cluster_means:
            distances.append( cosine_dist(feature_vector, mean_vector) )

        min_idx = min(enumerate(distances), key=itemgetter(1))[0]    
        test_features_clusters[min_idx].append(test_features_list[idx])
        test_labels_clusters[min_idx].append(test_labels_list[idx])

    return test_features_clusters, test_labels_clusters



