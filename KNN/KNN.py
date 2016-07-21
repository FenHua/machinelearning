#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
from numpy import *
import operator
from os import listdir
def createDataSet():
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels=['A','A','B','B']
    return group,labels
def classify0(inx,dataSet,labels,K):
    dataSetSize=dataSet.shape[0] # 返回其有多少个元素
    diffMat=tile(inx,(dataSetSize,1))-dataSet
    # Construct an array by repeating A the number of times given by reps.
    sqDiffMat=diffMat**2
    sqDistances=sqDiffMat.sum(axis=1)
    '''np.sum([[0, 1], [0, 5]], axis=0)
        array([0, 6])
      np.sum([[0, 1], [0, 5]], axis=1)
        array([1, 5])
        '''
    distances=sqDistances**0.5
    sortedDistIndicies=distances.argsort()# argsort函数返回的是数组值从小到大的索引值
    classCount={}
    for i in range(K):
        voteIlabel=labels[sortedDistIndicies[i]]
        classCount[voteIlabel]=classCount.get(voteIlabel,0)+1
        '''
            get()方法返回给定键的值。如果键不可用，则返回默认值None。
            dict.get(key, default=None)
            key -- 这是要搜索在字典中的键。
            default -- 这是要返回键不存在的的情况下默认值
            '''
        sortedClassCount=sorted(classCount.iteritems(),key=operator.itemgetter(1),reverse=True)
        #导入运算符模块的itemgetter方法，按照第二个元素的次序对元组进行排序
        return sortedClassCount[0][0]
def file2matrix(filename):
    fr=open(filename)
    arrayOLines=fr.readlines()
    numberOfLines=len(arrayOLines)
    returnMat=zeros((numberOfLines,3))
    classLabelVector=[]
    index=0
    for line in arrayOLines:
        line=line.strip()#去掉两边换行符(回车符)
        listFromLine=line.split('\t')#tab
        returnMat[index,:]=listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1]))#-1 返回最后一个元素
        index+=1
    return returnMat,classLabelVector
def autoNorm(dataSet):
    minVals=dataSet.min(0)#每列最小值
    maxVals=dataSet.max(0)
    ranges=maxVals-minVals
    normDataSet=zeros(shape(dataSet))
    m=dataSet.shape[0]
    normDataSet=dataSet-tile(minVals,(m,1))
    normDataSet=normDataSet/tile(ranges,(m,1))
    return normDataSet,ranges,minVals
def datingClassTest(filename):
    hoRatio=0.10
    datingDataMat,datingLabels=file2matrix(filename)
    normMat,ranges,minVals=autoNorm(datingDataMat)
    m=normMat.shape[0]
    numTestVecs=int(m*hoRatio)
    errorCount=0.0
    for i in range(numTestVecs):
        classifierResult=classify0(normMat[i,:],normMat[numTestVecs:m,:],datingLabels[numTestVecs:m],3)
        print("the classifier came back with:%d,the real answer is:%d"%(classifierResult,datingLabels[i]))
        if(classifierResult != datingLabels[i]):errorCount+=1.0
    print("the total error rate is:%f"%(errorCount/float(numTestVecs)))
'''
#########################################################
                  手写字识别
#########################################################
'''
def img2vector(filename):
    returnVect=zeros((1,1024))
    fr=open(filename)
    for i in range(32):
        linestr=fr.readline()
        for j in range(32):
            returnVect[0,32*i+j]=int(linestr[j])
    return returnVect
def handwritingClassTest():
    hwLabels=[]
    trainingFileList=listdir("trainingDigits")
    m=len(trainingFileList)
    trainingMat=zeros((m,1024))
    for i in range(m):
        fileNameStr=trainingFileList[i]
        fileStr=fileNameStr.split(".")[0]
        classNumStr=int(fileStr.split("_")[0])
        hwLabels.append(classNumStr)
        trainingMat[i,:]=img2vector("trainingDigits/%s"%fileNameStr)
    testFileList=listdir("testDigits")
    errorCount=0.0
    mTest=len(testFileList)
    for i in range(mTest):
        fileNameStr=testFileList[i]
        fileStr=fileNameStr.split(".")[0]
        classNumStr=int(fileStr.split('_')[0])
        vectorUnderTest=img2vector("testDigits/%s"%fileNameStr)
        classifierResult=classify0(vectorUnderTest,trainingMat,hwLabels,3)
        print("the classifier came back with:%d,the real answer is: %d"%(classifierResult,classNumStr))
        if(classifierResult != classNumStr):
            errorCount+=1.0
    print("\nthe total number of error is: %d"%errorCount)
    print("\nthe total error rate is: %f"%(errorCount/mTest))
            
    
