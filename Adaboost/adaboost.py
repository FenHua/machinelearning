# This Python file uses the following encoding: utf-8
import os, sys
from numpy import *
def loadSimpData():
    datMat=matrix([[1.,2.1],[2.,1.1],[1.3,1.],[1.,1.],[2.,1.]])
    classLabels=[1.0,1.0,-1.0,-1.0,1.0]
    return datMat,classLabels
def loadDataSet(filename):
    numFeat=len(open(filename).readline().split('\t'))
    dataMat=[];labelMat=[]
    fr=open(filename)
    for line in fr.readlines():
        lineArr=[]
        curLine=line.strip().split('\t')
        for m in range(numFeat-1):
            lineArr.append(float(curLine[m]))
        dataMat.append(lineArr)
        labelMat.append(float(curLine[-1]))
    return dataMat,labelMat
#        单层决策树
def stumpClassify(dataMatrix,dimen,threshVal,threshIneq):
    retArray=ones((shape(dataMatrix)[0],1))
    if threshIneq=='lt':
        retArray[dataMatrix[:,dimen]<=threshVal]=-1.0
    else:
        retArray[dataMatrix[:,dimen]>threshVal]=-1.0
    return retArray
def buildStump(dataArr,classLabels,D):
    dataMatrix=mat(dataArr);labelMat=mat(classLabels).T
    m,n=shape(dataMatrix)
    numSteps=10.0;bestStump={};bestClasEst=mat(zeros((m,1)))
    #bestStump用于存储给给定权重D时所得到的最佳单层决策树
    minError=inf
    for i in range(n):
        rangeMin=dataMatrix[:,i].min();rangeMax=dataMatrix[:,i].max()
        stepSize=(rangeMax-rangeMin)/numSteps#numSteps用于在特征的所有可能值上进行遍历
        for j in range(-1,int(numSteps)+1):
            for inequal in ["lt","gt"]:
                threshVal=(rangeMin+float(j)*stepSize)
                predictedVals=stumpClassify(dataMatrix,i,threshVal,inequal)
                errArr=mat(ones((m,1)))
                errArr[predictedVals==labelMat]=0
                weightedError=D.T*errArr
                #错误向量errArr和权重向量D的相应元素的相乘并求和，得weightError
                print("split:dim%d,thresh%.2f,thresh ineqal:%s,the weighted error is %.3f"%(i,threshVal,inequal,weightedError))
                if weightedError<minError:
                    minError=weightedError
                    bestClassEst=predictedVals.copy()
                    bestStump['dim']=i
                    bestStump['thresh']=threshVal
                    bestStump['ineq']=inequal
    return bestStump,minError,bestClassEst
def adaBoostTrainDs(dataArr,classLabels,numIt=40):
    #DS :decision stump
    weakClassArr=[]
    m=shape(dataArr)[0]
    D=mat(ones((m,1))/m)#初始化开始权值
    aggClassEst=mat(zeros((m,1)))#记录每个数据点的类别估计累计值
    for i in range(numIt):
        bestStump,error,classEst=buildStump(dataArr,classLabels,D)
        print("D:",D.T)
        alpha=float(0.5*log((1-error)/max(error,1e-16)))#log默认以e为底
        bestStump['alpha']=alpha
        weakClassArr.append(bestStump)
        print("classEst:",classEst.T)
        expon=multiply(-1*alpha*mat(classLabels).T,classEst)
        D=multiply(D,exp(expon))
        D=D/D.sum()
        aggClassEst+=alpha*classEst
        print("aggClassEst:",aggClassEst.T)
        aggErrors=multiply(sign(aggClassEst)!=mat(classLabels).T,ones((m,1)))
        errorRate=aggErrors.sum()/m
        print("total error:",errorRate,'\n')
        if errorRate==0.0:break
    return weakClassArr,aggClassEst
def adaClassify(datToClass,classifierArr):
    #datToClass 表示待分类的样例
    #classifierArr 已经训练好的弱分类器
    dataMatrix=mat(datToClass)
    m=shape(dataMatrix)[0]
    aggClassEst=mat(zeros((m,1)))
    for i in range(len(classifierArr)):
        classEst=stumpClassify(dataMatrix,classifierArr[i]['dim'],classifierArr[i]['thresh'],classifierArr[i]['ineq'])
        aggClassEst+=classifierArr[i]['alpha']*classEst
        print aggClassEst
    return sign(aggClassEst)
def plotROC(predStrengths,classLabels):
    #predStrengths分类器预测强度
    import matplotlib.pyplot as plt
    cur=(1.0,1.0)#初始点
    ySum=0.0
    numPosClas=sum(array(classLabels)==1.0)
    yStep=1/float(numPosClas)
    xStep=1/float(len(classLabels)-numPosClas)
    sortedIndicies=predStrengths.argsort()#得到排序索引，原数据从小到大
    fig=plt.figure()
    fig.clf()
    ax=plt.subplot(111)
    for index in sortedIndicies.tolist()[0]:
        #用tolist（）进行迭代循环
        if classLabels[index]==1.0:
            delx=0;dely=yStep
        else:
            delx=xStep;dely=0
            ySum+=cur[1]
        ax.plot([cur[0],cur[0]-delx],[cur[1],cur[1]-dely],c='b')
        cur=(cur[0]-delx,cur[1]-dely)
    ax.plot([0,1],[0,1],'b--')
    plt.xlabel('False Positive Rate');plt.ylabel('True Positive Rate')
    plt.title('ROC curve for AdaBoost Horse Colic Detection System')
    ax.axis([0,1,0,1])#用axis（xmin，xmax，ymin，ymax）限制横纵坐标
    plt.show()
    print ("the Area Under the Curve is:",ySum*xStep)



















