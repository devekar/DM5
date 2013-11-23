'''
Created on Nov 22, 2013

@author: Akshay
'''
import sys

def read_big_tm(tmpath):
    f = open(tmpath)
    tmlines = f.readlines()
    f.close()
    tm = []
    for line in tmlines:
        line = map(int, line.split())
        tm.append(line)
    return tm

def read_cluster_indices(cipath):
    f = open(cipath)
    cilines = f.readlines()
    f.close()
    ci = []
    for line in cilines:
        line = map(int, line.split())
        ci.append(line)
    return ci
    

def create_cluster_tms(big_tmpath, cipath):
    tm = read_big_tm(big_tmpath)
    cilines = read_cluster_indices(cipath)
    cluster_tms = []
    for i in xrange(len(cilines)):
        cluster_tms.append([])
    for c_idx, cluster in enumerate(cilines):
        for index in cluster:
            cluster_tms[c_idx].append(tm[index])
    return cluster_tms


def main(argv):
    create_cluster_tms(argv[1], argv[2])

if __name__ == '__main__':
    main(sys.argv)
