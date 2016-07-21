# This Python file uses the following encoding: utf-8
import os, sys
from numpy import *
def loadDataSet(fileName,delim='\t'):
    fr=open(fileName)
    stringArr=[line.strip().split(delim) for line in fr.readlines()]
    datArr=[map(float,line) for line in stringArr]
    return mat(datArr)
def pca(dataMat,topNfeat=99999):
    meanVals=mean(dataMat,axis=0)#按列求平均值
    meanRemoved=dataMat-meanVals
    #计算协方差矩阵
    covMat=cov(meanRemoved,rowvar=0)
    eigVals,eigVects=linalg.eig(mat(covMat))
    eigValInd=argsort(eigVals)#返回数组从小到大的索引
    eigValInd=eigValInd[:-(topNfeat+1):-1]#颠倒顺序
    redEigVects=eigVects[:,eigValInd]
    lowDDataMat=meanRemoved*redEigVects
    reconMat=(lowDDataMat*redEigVects.T)+meanVals
    return lowDDataMat,reconMat
def replaceNanWithMean():
    datMat=loadDataSet("C:\Users\YAN\Desktop\Pca/secom.data"," ")
    numFeat=shape(datMat)[1]
    for i in range(numFeat):
        meanVal=mean(datMat[nonzero(~isnan(datMat[:,i].A))[0],i])
        datMat[nonzero(isnan(datMat[:,i].A))[0],i]=meanVal
    return datMat

