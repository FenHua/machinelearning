# This Python file uses the following encoding: utf-8
import os, sys
import kMeans
from numpy import *
reload(kMeans)
'''
datMat=mat(kMeans.loadDataSet("C:\Users\YAN\Desktop\Kmeans/testSet.txt"))
print (kMeans.randCent(datMat,2))
print (kMeans.distEclud(datMat[0],datMat[1]))
myCentroids,clustAssing=kMeans.kMeans(datMat,4)
print ("the centroids are:",myCentroids)
print ("the assignment is:",clustAssing)
'''
'''
#-----------二分法Kmeans-------------#
datMat3=mat(kMeans.loadDataSet("C:\Users\YAN\Desktop\Kmeans/testSet2.txt"))
centList,myNewAssments=kMeans.biKmeans(datMat3,3)
print [centList[0],centList[1],centList[2]]
'''
#geoResults=kMeans.geoGrab('1 VA Center','Augusta, ME')
kMeans.clusterClubs(5)









