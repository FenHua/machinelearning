# This Python file uses the following encoding: utf-8
import os, sys
import regTrees
from numpy import*
reload(regTrees)
'''
testMat=mat(eye(4))
print testMat
mat0,mat1=regTrees.binSplitDataSet(testMat,1,0.5)
print mat0
print mat1
'''
'''
myDat=regTrees.loadDataSet('C:\Users\YAN\Desktop\Cart\ex00.txt')
myMat=mat(myDat)
retTree=regTrees.createTree(myMat)
print retTree
'''
'''
myDat1=regTrees.loadDataSet('C:\Users\YAN\Desktop\Cart\ex0.txt')
myMat1=mat(myDat1)
print regTrees.createTree(myMat1)
'''
'''
myDat=regTrees.loadDataSet('C:\Users\YAN\Desktop\Cart\ex2.txt')
myMat=mat(myDat)
myTree=regTrees.createTree(myMat,ops=(0,1))
myDat1=regTrees.loadDataSet('C:\Users\YAN\Desktop\Cart\ex2test.txt')
myMatTest=mat(myDat1)
tree=regTrees.prune(myTree,myMatTest)
print tree
'''
'''
myDat=mat(regTrees.loadDataSet('C:\Users\YAN\Desktop\Cart\exp2.txt'))
myTree=regTrees.createTree(myDat,regTrees.modelLeaf,regTrees.modelErr,(1,10))
print myTree
'''
trainMat=mat(regTrees.loadDataSet('C:\Users\YAN\Desktop\Cart/bikeSpeedVsIq_train.txt'))
testMat=mat(regTrees.loadDataSet('C:\Users\YAN\Desktop\Cart/bikeSpeedVsIq_test.txt'))
myTree=regTrees.createTree(trainMat,ops=(1,20))#ops前者表示错误缩小最小期望，后者表示最小分割数量
yHat=regTrees.createForeCast(myTree,testMat[:,0])
print corrcoef(yHat,testMat[:,1],rowvar=0)[0,1]
'''
If `rowvar` is non-zero (default), then each row represents a
        variable, with observations in the columns. Otherwise, the relationship
        is transposed: each column represents a variable, while the rows
        contain observations.
'''
myTree1=regTrees.createTree(trainMat,regTrees.modelLeaf,regTrees.modelErr,(1,20))
yHat=regTrees.createForeCast(myTree,testMat[:,0],regTrees.modelTreeEval)
print corrcoef(yHat,testMat[:,1],rowvar=0)
 



















