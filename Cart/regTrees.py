# This Python file uses the following encoding: utf-8
import os, sys
class treeNode():
    def __init__(self,feat,val,right,left):
        featureToSplitOn=feat
        valueOfSplit=val
        rightBranch=right
        leftBranch=left

from numpy import *
def loadDataSet(fileName):
    dataMat=[]
    fr=open(fileName)
    for line in fr.readlines():
        curLine=line.strip().split('\t')
        fltLine=map(float,curLine)#返回一个由float函数处理后的list
        dataMat.append(fltLine)
    return dataMat
def binSplitDataSet(dataSet,feature,value):
    mat0=dataSet[nonzero(dataSet[:,feature]>value)[0],:][0]#排列成数组
    mat1=dataSet[nonzero(dataSet[:,feature]<=value)[0],:][0]
    return mat0,mat1
def regLeaf(dataSet):
    return mean(dataSet[:,-1])#负责生产叶节点，在回归树中，该模型其实就是目标变量的均值
def regErr(dataSet):
    return var(dataSet[:,-1])*shape(dataSet)[0]#总的方差
def createTree(dataSet,leafType=regLeaf,errType=regErr,ops=(1,4)):
    feat,val=chooseBestSplit(dataSet,leafType,errType,ops)
    if feat==None:return val
    retTree={}
    retTree['spInd']=feat
    retTree['spVal']=val
    lSet,rSet=binSplitDataSet(dataSet,feat,val)
    retTree['left']=createTree(lSet,leafType,errType,ops)
    retTree['right']=createTree(rSet,leafType,errType,ops)
    return retTree
def chooseBestSplit(dataSet,leafType=regLeaf,errType=regErr,ops=(1,4)):
    tolS=ops[0];tolN=ops[1]
    #tolS也许误差下降值，tolN切分的最小样本数
    if len(set(dataSet[:,-1].T.tolist()[0]))==1:
        return None,leafType(dataSet)
    m,n=shape(dataSet)
    S=errType(dataSet)#计算目标变量的方差
    bestS=inf;bestIndex=0;bestValue=0
    for featIndex in range(n-1):
        for splitVal in set(dataSet[:,featIndex]):
            mat0,mat1=binSplitDataSet(dataSet,featIndex,splitVal)
            if(shape(mat0)[0]<tolN)or(shape(mat1)<tolN):continue
            news=errType(mat0)+errType(mat1)
            if news<bestS:
                bestIndex=featIndex
                bestValue=splitVal
                bestS=news
    if(S-bestS)<tolS:
        return None,leafType(dataSet)#如果误差减少太小则直接创建叶节点
    mat0,mat1=binSplitDataSet(dataSet,bestIndex,bestValue)
    if(shape(mat0)[0]<tolN)or(shape(mat1)[0]<tolN):
        return None,leafType(dataSet)
    return bestIndex,bestValue
#----------------------后剪枝------------------#
def isTree(obj):
    return (type(obj).__name__=='dict')
def getMean(tree):
    if isTree(tree['right']):tree['right']=getMean(tree['right'])
    if isTree(tree['left']):tree['left']=getMean(tree['left'])
    return (tree['right']+tree['left'])/2
def prune(tree,testData):
    #prune 精简，修剪
    if shape(testData)[0]==0:return getMean(tree)
    #没有测试数据时对树进行塌陷处理
    if(isTree(tree['left']) or isTree(tree['right'])):
        lSet,rSet=binSplitDataSet(testData,tree['spInd'],tree['spVal'])
    if isTree(tree['left']):tree['left']=prune(tree['left'],lSet)
    if isTree(tree['right']):tree['right']=prune(tree['right'],rSet)
    if not isTree(tree['left']) and not isTree(tree['right']):
        lSet,rSet=binSplitDataSet(testData,tree['spInd'],tree['spVal'])
        errorNomerge=sum(power(lSet[:,-1]-tree['left'],2))+sum(power(rSet[:,-1]-tree['right'],2))
        treeMean=(tree['left']+tree['right'])/2.0
        errorMerge=sum(power(testData[:,-1]-treeMean,2))
        if errorMerge<errorNomerge:
            print "merging"
            return treeMean
        else:
            return tree
    else:
        return tree
def linearSolve(dataSet):
    m,n=shape(dataSet)
    X=mat(ones((m,n)));Y=mat(ones((m,1)))
    X[:,1:n]=dataSet[:,0:n-1];Y=dataSet[:,-1]
    #X,Y数据格式化
    xTx=X.T*X
    print linalg.det(xTx)
    if linalg.det(xTx)==0.0:
        raise NameError('this matrix is singular,cannot do inverse,\n\
try increasing the second value of ops')
    ws=xTx.I*(X.T*Y)
    return ws,X,Y
def modelLeaf(dataSet):
    ws,X,Y=linearSolve(dataSet)
    return ws
def modelErr(dataSet):
    ws,X,Y=linearSolve(dataSet)
    yHat=X*ws
    return sum(power(Y-yHat,2))
def regTreeEval(model,inDat):
    return float(model)
def modelTreeEval(model,inDat):
    n=shape(inDat)[1]
    X=mat(ones((1,n+1)))
    X[:,1:n+1]=inDat
    return float(X*model)
def treeForeCast(tree,inData,modelEval=regTreeEval):
    if not isTree(tree):return modelEval(tree,inData)#将树浮点化
    if inData[tree['spInd']]>tree['spVal']:
        if isTree(tree['left']):
            return treeForeCast(tree['left'],inData,modelEval)
        else:
            return modelEval(tree['left'],inData)
    else:
        if isTree(tree['right']):
            return treeForeCast(tree['right'],inData,modelEval)
        else:
            return modelEval(tree['right'],inData)

def createForeCast(tree,testData,modelEval=regTreeEval):
    m=len(testData)
    yHat=mat(zeros((m,1)))
    for i in range(m):
        yHat[i,0]=treeForeCast(tree,mat(testData[i]),modelEval)
    return yHat

            



































