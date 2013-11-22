'''
Created on Nov 4, 2013

@author: Akshay
'''
import csv
import sys
from Kmeans import KMeans

def parseDM(filepath = r'data_matrix.csv'):
    dataMatrix = []

    matrix = []
    word_list = []
    topic_list = []
    place_list = []
    with open(filepath, 'rb') as csv_file:
        reader = csv.reader(csv_file, delimiter=',', quotechar='"')
        for row in reader:
            dataMatrix.append(row)

    for item in dataMatrix[1]:
        if "_" not in item:
            word_list.append(item)
        elif "t_" in item:
            topic_list.append(item[2:])
        elif "p_" in item:
            place_list.append(item[2:])

    word_list = word_list[1:] # Remove 'Article #'
    words_topics_size = len(topic_list) + len(word_list)

    for row in dataMatrix[2:]:
        matrix.append( [row[0]] + map(int, row[1:]) )
    return {"topic_list":topic_list, "word_list": word_list, "place_list":place_list, "matrix": matrix}


def write_clusters(clusters):
	f = open("Kmeans_clusters.txt", "w")
	for cluster in clusters:
		f.write(' '.join(map(str,cluster)))
		f.write('\n')
	f.close()


''' Main '''

data = parseDM()
clusters = int(sys.argv[1])
dist_type = int(sys.argv[2])
kmeans = KMeans(clusters, dist_type, data)
clusters_ind = kmeans.get_clusters()
write_clusters(clusters_ind)
