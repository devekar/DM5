'''
Created on Nov 4, 2013

@author: Akshay
'''

from __future__ import division
import timeit
import math
import itertools
import random
import copy

class KMeans(object):
    K = None
    dist_type = None
    word_list = None
    topic_list = None
    place_list = None
    dataset = None
    magnitudes = None
    clusters = None
    cluster_means = None
    epsilon = 0.00001

    def __init__(self, k, d, data):
        self.K = k
        self.dist_type = d
        self.word_list = data["word_list"]
        self.topic_list = data["topic_list"]
        self.place_list = data["place_list"]
        self.dataset = data["matrix"]
        if self.dist_type == 0:
            self.magnitudes = [None]*len(self.dataset)
            time1 = timeit.default_timer()
            self.computeMagnitudes()
            time2 = timeit.default_timer()
            print "Magnitudes computed in time: ", str(time2 - time1)
        
        
    def computeMagnitudes(self):
        for idx, i in enumerate(self.dataset):
            self.magnitudes[idx] = self.magnitude(i[1:len(self.word_list)+1])


    '''Compute magnitude of a vector'''
    def magnitude(self, vector):
        mag = 0;
        for item in vector:
            mag += item * item
        mag = math.sqrt(mag)
        return mag;
    
    
    '''Compute cosine distance between two numeric vectors'''
    def cosine_dist(self, record_idx, cluster_idx):
        dot_product = 0;
        vector1 = self.dataset[record_idx][1:len(self.word_list) + 1]
        vector2 = self.cluster_means[cluster_idx]
        for i1, i2 in itertools.izip(vector1, vector2):
            dot_product += i1 * i2;
        mag1 = 1
        mag2 = 1
        if dot_product > 0:
            mag1 = self.magnitudes[record_idx];
            mag2 = self.magnitude(self.cluster_means[cluster_idx]);
        cosine_sim = dot_product / (mag1 * mag2)
        cosine_dist = 1 - cosine_sim 
        return cosine_dist
    
    
    def cosine_dist_means(self, vector1, vector2):
        dot_product = 0;
        for i1, i2 in itertools.izip(vector1, vector2):
            dot_product += i1 * i2;
        mag1 = 1
        mag2 = 1
        if dot_product > 0:
            mag1 = self.magnitude(vector1);
            mag2 = self.magnitude(vector2);
        cosine_sim = dot_product / (mag1 * mag2)
        cosine_dist = 1 - cosine_sim 
        return cosine_dist
    
    
    '''Compute Euclidean distance between two numeric vectors'''
    def euclidean_dist(self, record_idx, cluster_idx):
        vec1 = self.dataset[record_idx][1:len(self.word_list) + 1]
        vec2 = self.cluster_means[cluster_idx]
        return math.sqrt(sum([(abs(a-b))**2 for a,b in zip(vec1,vec2)]))
    
    
    def euclidean_dist_means(self, vec1, vec2):
        return math.sqrt(sum([(abs(a-b))**2 for a,b in zip(vec1,vec2)]))
    
    
    def get_mean(self, vector):
        return sum(vector) / len(vector)
    
    
    def get_mean_vector(self, list):
        vectors = []
        for item in list:
            trimmed = item[1:len(self.word_list)+1]
            vectors.append(trimmed)
        return map(self.get_mean, zip(*vectors))
    
    def get_cluster_mean_vector(self, list):
        return map(self.get_mean, zip(*list))
    
    
    '''Main Algorithm'''
    def get_clusters(self):
        kmeans_start = timeit.default_timer()
        '''Start with random cluster means'''
        samples = random.sample(self.dataset, 1000)
        sample_mean = self.get_mean_vector(samples)
        self.cluster_means = [[] for i in xrange(self.K)]
        for i in xrange(self.K):
            for j in xrange(len(self.word_list)):
                self.cluster_means[i].append(sample_mean[j] + random.random())
        '''Main loop'''
        for i in xrange(1000):
            print "Starting iteration " + str(i)
            '''Assign points to the nearest cluster'''
            self.clusters = [[] for j in xrange(self.K)]
            cluster_indices = [[] for j in xrange(self.K)]
            for idx,point in enumerate(self.dataset):
                distances = []
                for k in xrange(self.K):
                    if self.dist_type == 0:
                        distances.append(self.cosine_dist(idx, k))
                    else:
                        distances.append(self.euclidean_dist(idx, k))
                closest_cluster = distances.index(min(distances))
                self.clusters[closest_cluster].append(point)
                cluster_indices[closest_cluster].append(idx)
            print [len(a) for a in self.clusters]
            '''Recompute centroids for each cluster'''
            old_cluster_means = copy.copy(self.cluster_means)
            for k in xrange(self.K):
                self.cluster_means[k] = self.get_mean_vector(self.clusters[k])
                #print "Mean " + str(k) + ": " + str(self.cluster_means[k])
            '''Check if means changed significantly'''
            if self.dist_type == 0:
                diff = [self.cosine_dist_means(new, old) for new,old in zip(self.cluster_means, old_cluster_means)]
            else:
                diff = [self.euclidean_dist_means(new, old) for new,old in zip(self.cluster_means, old_cluster_means)]
            print "diff = " + str(diff)
            if sum(diff) <= self.epsilon:
                print "Converged in " + str(i+1) + " iterations"
                break
        kmeans_stop = timeit.default_timer()
        print "K-means converged in time: " + str(kmeans_stop - kmeans_start) + " seconds or " + str((kmeans_stop - kmeans_start) / 60) + " minutes"
        self.entropy()
        return cluster_indices
        
        
        '''compute entropy'''
    def entropy(self):
        topic_start = len(self.word_list) + 1
        topic_end = topic_start + len(self.topic_list)
        place_start = topic_end
        place_end = place_start + len(self.place_list)
        cluster_entropies = [[0 for i in xrange(place_end-topic_start)] for j in xrange(self.K)]
        cluster_labeled_sizes = []
        for k in xrange(self.K):
            for point in self.clusters[k]:
                vec = copy.copy(point[topic_start:place_end])
                if sum(vec) > 0:
                    vec = [a/sum(vec) for a in vec]
                    cluster_entropies[k] = [a+b for a,b in zip(cluster_entropies[k], vec)]
            cluster_labeled_sizes.append(sum(cluster_entropies[k]))
            cluster_entropies[k] = [a/sum(cluster_entropies[k]) for a in cluster_entropies[k]]
            cluster_entropies[k] = [(-1)*p*(math.log(p,2)) if p>0 else 0 for p in cluster_entropies[k]]
            cluster_entropies[k] = sum(cluster_entropies[k])
        cluster_weights = [a/sum(cluster_labeled_sizes) for a in cluster_labeled_sizes]
        entropy = sum([a*b for a,b in zip(cluster_weights, cluster_entropies)])
        print "Entropy = " + str(entropy)
                
