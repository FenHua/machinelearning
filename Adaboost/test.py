import adaboost
reload(adaboost)
from numpy import *
datMat,classLabels=adaboost.loadSimpData()
'''
D=mat(ones((5,1))/5)
bestStump,minError,bestClassEst=adaboost.buildStump(datMat,classLabels,D)
print bestStump
print minError
print bestClassEst
'''
'''
classifierArray=adaboost.adaBoostTrainDs(datMat,classLabels,40)
print classifierArray
result=adaboost.adaClassify([0,0],classifierArray)
print result
'''

datArr,labelArr=adaboost.loadDataSet('C:\Users\YAN\Desktop\Adaboost/horseColicTraining.txt')
classifierArray,aggClassEst=adaboost.adaBoostTrainDs(datArr,labelArr,10)
'''
testArr,testLabelArr=adaboost.loadDataSet('C:\Users\YAN\Desktop\Adaboost/horseColicTest.txt')
prediction=adaboost.adaClassify(testArr,classifierArray)
errArr=mat(ones((67,1)))
result=errArr[prediction!=mat(testLabelArr).T].sum()
print result
'''
adaboost.plotROC(aggClassEst.T,labelArr)
