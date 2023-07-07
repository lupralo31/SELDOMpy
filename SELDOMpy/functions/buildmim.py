import numpy as np
# Package needed to perform histograms
from sklearn.metrics import mutual_info_score
# Package needed to calculate mutual information
from math import sqrt, ceil
# "sqrt" is imported to be able to solve square roots
# "ceil" is imported to be able to round up


# Function to calculate mutual information between 2 nodes from 2 lists of measures
def calc_mi(x, y, nbins):
    if nbins == 0:
        bins = ceil(sqrt(len(x)*2))
    else:
        bins = nbins
    c_xy = np.histogram2d(x, y, bins)[0]
    mi = mutual_info_score(None, None, contingency=c_xy)
    return mi


# Function to calculate the adjacency matrix from "conc_data"
def buildmim(conc_data, nbins=0):
    # "adjMat" will consist of 4 lists representing the 4 rows of the R program matrix
    # You can specify the number of bins for the discretization of the measures
    adjMat = []
    dataArray = []
    for i in range(len(conc_data[0])):
        adjMat.append([])
        dataArray.append([])

    for i in range(len(conc_data[0])):  # Scroll through columns
        for j in range(len(conc_data)):  # Rows of each column are traversed
            dataArray[i].append(conc_data[j][i])

    for i in range(len(dataArray)):
        for j in range(len(dataArray)):
            mi = calc_mi(dataArray[i], dataArray[j], nbins)
            adjMat[i].append(mi)
    maxvalue = 0

    for i in range(len(adjMat)):
        for j in range(len(adjMat[i])):
            if adjMat[i][j] > maxvalue:
                maxvalue = adjMat[i][j]

    for i in range(len(adjMat)):
        for j in range(len(adjMat[i])):
            if i == j:
                adjMat[i][j] = 0
            else:
                adjMat[i][j] = round(adjMat[i][j]/maxvalue, 8)

    return adjMat
