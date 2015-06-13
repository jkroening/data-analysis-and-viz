import csv
import numpy as np
import ast
import scipy.cluster.hierarchy as sch
from sklearn import preprocessing
import pylab as pl
from jellyfish import jaro_distance
from unidecode import unidecode
import matplotlib.pyplot as plt
from collections import defaultdict
import time
import Levenshtein as lev
import nltk
from nltk.corpus import brown
import sys

start_time = time.time()

def d(coord):
    i, j = coord
    return lev.distance(tags[i], tags[j])

def main(f, level, tags):

    for i in f:
        for t in ast.literal_eval(i['tags']):
            t.encode('ascii', 'ignore')
            tags.append(t.lower().replace(' ', '').replace(',', '').replace('.', ''))

    unique_tags = list(set(tags))
    tags = unique_tags

    dists = np.triu_indices(len(tags), 1)
    data_dist = np.apply_along_axis(d, 0, dists)
    # print data_dist
    # min_max_scaler = preprocessing.MinMaxScaler()
    # data_dist_norm = min_max_scaler.fit_transform(data_dist)

    data_link = sch.linkage(data_dist, method='complete')
    sch.dendrogram(data_link,labels=tags)
    # data_clust = sch.fcluster(data_link, 0.5*data_dist.max())
    data_clust = sch.fcluster(data_link, level)

    buckets = defaultdict(list)
    for i in range(len(tags)):
        clustID = data_clust[i]
        tag = tags[i]
        if not tag in buckets[clustID]:
            buckets[clustID].append(tag)

    print buckets

    print time.time() - start_time, "seconds"

    plt.xlabel('Tags')
    plt.ylabel('Distance')
    plt.suptitle('Tags clustering', fontweight='bold', fontsize=14)
    plt.show()

if __name__=="__main__":
    tags = []

    # csv file for clustering
    with open(sys.argv[1], 'rU') as csvFile:
        f = csv.DictReader(csvFile, dialect='excel')

        # level of clustering, recommended between 0.5 and 1.0
        level = float(sys.argv[2])

        main(f, level, tags)
