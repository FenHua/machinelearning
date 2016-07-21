# This Python file uses the following encoding: utf-8
import os, sys
from numpy import *
def loadDataSet():
    postingList=[['my','dog','has','flea','problems','help','please'],\
                 ['maybe','not','take','him','to','dog','park','stupid'],\
                 ['my','dalmation','is','so','cute','I','love','him'],\
                 ['stop','posting','stupid','worthless','garbage'],\
                 ['mr','licks','ate','my','steak','how','to','stop','him'],\
                 ['guit','buying','worthless','dog','food','stupid']]
    classVec=[0,1,0,1,0,1] #1代表侮辱性文字，0代表正常言论
    return postingList,classVec
#创建词汇表
def createVocabList(dataSet):
    vocabSet=set([])
    for document in dataSet:
        vocabSet=vocabSet|set(document)
    return list(vocabSet)#转换为列表，方便后面index属性的使用
def setOfWord2Vec(vocabList,inputSet):
    returnVec=[0]*len(vocabList)#创建一个与词汇表等长的向量，并且将其元素设置为0
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)]=1
        else:
            print ("the word:%s is not in my Vocabulary!"%word)
    return returnVec
'''
def trainNB0(trainMatrix,trainCategory):
    numTrainDocs=len(trainMatrix)
    numwords=len(trainMatrix[0])
    pAbusive=sum(trainCategory)/float(numTrainDocs)#针对只有两个类别且类别对应0，1而言
    p0Num=zeros(numwords);p1Num=zeros(numwords)# 只有一个变量是zeros只创建一个一维数组
    p0Denom=0.0;p1Denom=0.0
    for i in range(numTrainDocs):
        if trainCategory[i]==1:
            p0Num+=trainMatrix[i]
            p0Denom+=sum(trainMatrix[i])
        else:
            p1Num+=trainMatrix[i]
            p1Denom+=sum(trainMatrix[i])
    p1Vect=p1Num/p1Denom #计算出在相应集合中的元素对应概率
    p0Vect=p0Num/p0Denom
    return p0Vect,p1Vect,pAbusive
'''
def trainNB1(trainMatrix,trainCategory):
    numTrainDocs=len(trainMatrix)
    numwords=len(trainMatrix[0])
    pAbusive=sum(trainCategory)/float(numTrainDocs)#针对只有两个类别且类别对应0，1而言
    p0Num=ones(numwords);p1Num=ones(numwords)# 只有一个变量是zeros只创建一个一维数组
    p0Denom=2.0;p1Denom=2.0
    for i in range(numTrainDocs):
        if trainCategory[i]==1:
            p0Num+=trainMatrix[i]
            p0Denom+=sum(trainMatrix[i])
        else:
            p1Num+=trainMatrix[i]
            p1Denom+=sum(trainMatrix[i])
    p1Vect=(p1Num/p1Denom) #计算出在相应集合中的元素对应概率
    p0Vect=(p0Num/p0Denom) #加入log函数会扩大数的表示，log只能接受单个参数
    return p0Vect,p1Vect,pAbusive
def classifyNB(vec2Classify,p0Vec,p1Vec,pClass1):
    p1=sum(vec2Classify*p0Vec)*pClass1
    p0=sum(vec2Classify*p1Vec)*(1-pClass1)
    if p1>p0:
        return 1
    else:
        return 0
def testingNB():
    listOPosts,listClasses=loadDataSet()
    myVocabList=createVocabList(listOPosts)
    trainMat=[]
    for postinDoc in listOPosts:
        trainMat.append(setOfWord2Vec(myVocabList,postinDoc))
    p0V,p1V,pAb=trainNB1(trainMat,listClasses)
    testEntry=['love','my','dalmation']
    thisDoc=array(setOfWord2Vec(myVocabList,testEntry))
    print(testEntry,"classified as",classifyNB(thisDoc,p0V,p1V,pAb))
    testEntry=['stupid','garbage']
    thisDoc=array(setOfWord2Vec(myVocabList,testEntry))
    print(testEntry,"calssified as",classifyNB(thisDoc,p0V,p1V,pAb))
def bagOfWords2VecMN(vocabList,inputSet):
    returnVec=[0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)]+=1
    return returnVec
def textParse(bigString):
    import re
    listOfTokens=re.split(r"\W*",bigString)
    return[tok.lower() for tok in listOfTokens if len(tok)>2]
import random
def spamTest():
    docList=[];classList=[];fullText=[]
    for i in range(1,26):
        wordList=textParse(open("C:\Users\YAN\Desktop\NB\email\spam/%d.txt"%i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList=textParse(open("C:\Users\YAN\Desktop\NB\email\ham/%d.txt"%i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList=createVocabList(docList)
    trainingSet=range(50)#生成一个整数列表
    testSet=[]
    for i in range(10):
        randIndex=int(random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])
    trainMat=[];trainClass=[]
    for docIndex in trainingSet:
        trainMat.append(setOfWord2Vec(vocabList,docList[docIndex]))
        trainClass.append(classList[docIndex])
    p0V,p1V,pSpam=trainNB1(array(trainMat),array(trainClass))#列表以字符串存储，所以转换为array
    errorCount=0.0
    for docIndex in testSet:
        wordVector=setOfWord2Vec(vocabList,docList[docIndex])
        if classifyNB(array(wordVector),p0V,p1V,pSpam)!=classList[docIndex]:
            errorCount+=1
    print("the error rate is: ",float(errorCount)/len(testSet))
#RSS源分类器及高频词去除函数
def calcMostFreq(vocabList,fullText):
    import operator
    freqDict={}
    for token in vocabList:
        freqDict[token]=fullText.count(token)
    sortedFreq=sorted(freqDict.iteritems(),key=operator.itemgetter(1),reverse=True)
    return sortedFreq[:30]
def localWords(feed1,feed0):
    import feedparser
    docList=[];classList=[];fullList=[]
    minLen=min(len(feed1['entries']),len(feed0['entries']))
    for i in range(minLen):
        wordList=textParse(feed1['entries'][i]['summary'])#每一次访问一条RSS源
        docList.append(wordList)
        fullList.extend(wordList)
        classList.append(1)
        wordList=textParse(feed0['entries'][i]['summary'])
        docList.append(wordList)
        fullList.extend(wordList)
        classList.append(0)
    vocabList=createVocabList(docList)
    top30Words=calcMostFreq(vocabList,fullList)
    for pairW in top30Words:
        if pairW[0] in vocabList:
            vocabList.remove(pairW[0])
    trainingSet=range(2*minLen);testSet=[]
    for i in range(20):
        randIndex=int(random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])
    trainMat=[];trainClasses=[]
    for docIndex in trainingSet:
        trainMat.append(bagOfWords2VecMN(vocabList,docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0V,p1V,pSpam=trainNB1(array(trainMat),array(trainClasses))
    errorCount=0
    for docIndex in testSet:
        wordVector=bagOfWords2VecMN(vocabList,docList[docIndex])
        if classifyNB(array(wordVector),p0V,p1V,pSpam)!=classList[docIndex]:
            errorCount+=1
    print("the error rate is :",float(errorCount)/len(testSet))
    return vocabList,p0V,p1V

def getTopWords(ny,sf):
    import operator
    vocabList,p0V,p1V=localWords(ny,sf)
    topNY=[];topSF=[]
    for i in range(len(p0V)):
        if p0V[i]>0.004:topSF.append((vocabList[i],p0V[i]))
        if p1V[i]>0.004:topNY.append((vocabList[i],p1V[i]))
    sortedSF=sorted(topSF,key=lambda pair:pair[1],reverse=True)
    print("SF************************************SF")
    for item in sortedSF:
        print item[0]
    sortedNY=sorted(topNY,key=lambda pair:pair[1],reverse=True)
    print("NY************************************NY")
    for item in sortedNY:
        print item[0]
        
    
        
    
        

    
