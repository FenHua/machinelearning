# This Python file uses the following encoding: utf-8
import os, sys
import regression
reload(regression)
from numpy import *
xArr,yArr=regression.loadDataSet('C:\Users\YAN\Desktop\\regression/ex0.txt')
'''
#---------标准回归----------#
print (xArr[0:2])
ws=regression.standRegres(xArr,yArr)
print ws
xMat=mat(xArr)
yMat=mat(yArr)
yHat=xMat*ws
import matplotlib.pyplot as pl
fig=pl.figure()
ax=fig.add_subplot(111)
ax.scatter(xMat[:,1].flatten().A[0],yMat.T[:,0].flatten().A[0])
xCopy=xMat.copy(0)# sort along the first axis
yHat=xCopy*ws
ax.plot(xCopy[:,1],yHat)
pl.show()
'''
#print(corrcoef(yHat.T,yMat))
'''
print yArr[0]
print(regression.lwlr(xArr[0],xArr,yArr,1.0))
print(regression.lwlr(xArr[0],xArr,yArr,0.001))
'''
'''
#----------局部回归--------#
yHat=regression.lwlrTest(xArr,xArr,yArr,0.003)
xMat=mat(xArr)
srtInd=xMat[:,1].argsort(0)
xSort=xMat[srtInd][:,0,:]
import matplotlib.pyplot as pl
fig=pl.figure()
ax=fig.add_subplot(111)
ax.plot(xSort[:,1].flatten().A[0],yHat[srtInd])#利用srtInd将yHat数组顺序调整
ax.scatter(xMat[:,1].flatten().A[0],mat(yArr).T.flatten().A[0],s=2,c='red')
pl.show()
'''
abX,abY=regression.loadDataSet('C:\Users\YAN\Desktop\\regression/abalone.txt')
'''
yHat01=regression.lwlrTest(abX[0:99],abX[0:99],abY[0:99],0.1)
yHat1=regression.lwlrTest(abX[0:99],abX[0:99],abY[0:99],1)
yHat10=regression.lwlrTest(abX[0:99],abX[0:99],abY[0:99],10)
print(regression.rssError(abY[0:99],yHat01))
print(regression.rssError(abY[0:99],yHat1))
print(regression.rssError(abY[0:99],yHat10))
#------------------------------------#
yHat01=regression.lwlrTest(abX[100:199],abX[0:99],abY[0:99],0.1)
yHat1=regression.lwlrTest(abX[100:199],abX[0:99],abY[0:99],1)
yHat10=regression.lwlrTest(abX[100:199],abX[0:99],abY[0:99],10)
print(regression.rssError(abY[100:199],yHat01.T))
print(regression.rssError(abY[100:199],yHat1.T))
print(regression.rssError(abY[100:199],yHat10.T))
ws=regression.standRegres(abX[0:99],abY[0:99])
yHat=mat(abX[100:199])*ws
print(regression.rssError(abY[100:199],yHat.T.A))
'''
'''
#---------------------岭回归-----------#
ridgeWeights=regression.ridgeTest(abX,abY)
import matplotlib.pyplot as plt
fig=plt.figure()
ax=fig.add_subplot(111)
ax.plot(ridgeWeights)
plt.show()
'''
#---------------向前逐步回归----------#
stage=regression.stageWise(abX,abY,0.005,1000)
import matplotlib.pyplot as plt
fig=plt.figure()
ax=fig.add_subplot(111)
ax.plot(stage)
plt.show()







