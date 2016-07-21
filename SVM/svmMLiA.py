# This Python file uses the following encoding: utf-8
import os, sys
from numpy import *
def loadDataSet(fileName):
    dataMat=[];labelMat=[]
    fr=open(fileName)
    for line in fr.readlines():
        lineArr=line.strip().split('\t')
        dataMat.append([float(lineArr[0]),float(lineArr[1])])
        labelMat.append(float(lineArr[2]))
    return dataMat,labelMat
def selectJrand(i,m):
    #只要函数值不等于输入值i，函数就会进行随机选择
    j=i
    while(j==i):
        j=int(random.uniform(0,m))
    return j
def clipAlpha(aj,H,L):
    #调整大于H或小于L的alpha值
    if aj>H:
        aj=H
    if L>aj:
        aj=L
    return aj
#简化后的SMO算法
def smoSimple(dataMatIn,classLabels,C,toler,maxIter):
    dataMatrix=mat(dataMatIn);labelMat=mat(classLabels).transpose()
    b=0;m,n=shape(dataMatrix)
    alphas=mat(zeros((m,1)))#拉格朗日乘子，alpha对应于每一个等式
    iter=0
    while(iter<maxIter):
        alphaPairsChanged=0
        for i in range(m):
            fxi=float((multiply(alphas,labelMat).T)*(dataMatrix*(dataMatrix[i,:].T)))+b
            #m*1 1*m m*n n*1
            Ei=fxi-float(labelMat[i])
            if((labelMat[i]*Ei<-toler)and(alphas[i]<C))or((labelMat[i]*Ei>toler)and(alphas[i]>0)):
                #toler 容错率  
                j=selectJrand(i,m)
                #随机选择第二个alpha
                fxj=float(multiply(alphas,labelMat).T*(dataMatrix*dataMatrix[j,:].T))+b
                Ej=fxj-float(labelMat[j])
                alphaIold=alphas[i].copy()
                alphaJold=alphas[j].copy()
                if(labelMat[i]!=labelMat[j]):
                    L=max(0,alphas[j]-alphas[i])
                    H=min(C,C+alphas[j]-alphas[i])#C为常数
                else:
                    L=max(0,alphas[j]+alphas[i]-C)
                    H=min(C,alphas[j]+alphas[i])
                if L==H:print "L==H";continue
                eta=2.0*dataMatrix[i,:]*dataMatrix[j,:].T-dataMatrix[i,:]*dataMatrix[i,:].T-dataMatrix[j,:]*dataMatrix[j,:].T
                #对j进行修改
                if eta>=0:print "eta>=0";continue
                alphas[j]-=labelMat[j]*(Ei-Ej)/eta
                alphas[j]=clipAlpha(alphas[j],H,L)
                if(abs(alphas[j]-alphaJold)<0.00001):print "j not moving enough";continue
                alphas[i]+=labelMat[j]*labelMat[i]*(alphaJold-alphas[j])
                b1=b-Ei-labelMat[i]*(alphas[i]-alphaIold)*dataMatrix[i,:]*dataMatrix[i,:].T-labelMat[j]*(alphas[j]-alphaJold)*dataMatrix[i,:]*dataMatrix[j,:].T
                b2=b-Ej-labelMat[i]*(alphas[i]-alphaIold)*dataMatrix[i,:]*dataMatrix[j,:].T-labelMat[j]*(alphas[j]-alphaJold)*dataMatrix[j,:]*dataMatrix[j,:].T
                if(0<alphas[i])and(C>alphas[i]):b=b1
                elif(0<alphas[j])and(C>alphas[j]):b=b2
                else: b=(b1+b2)/2.0
                alphaPairsChanged+=1
                print("iter: %d i: %d,pairs changed %d"%(iter,i,alphaPairsChanged))
        if(alphaPairsChanged==0):iter+=1
        else: iter=0
        print("iteration number: %d"%iter)
    return b,alphas
class optStruct:
    def __init__(self,dataMatIn,classLabels,C,toler,kTup):
        self.X=dataMatIn
        self.labelMat=classLabels
        self.C=C
        self.tol=toler
        self.m=shape(dataMatIn)[0]
        self.alphas=mat(zeros((self.m,1)))
        self.b=0
        self.eCache=mat(zeros((self.m,2)))#误差缓存，第一列给出eCache是否有效的标志，而第二列给出是实际的E值
        self.k=mat(zeros((self.m,self.m)))
        for i in range(self.m):
            self.k[:,i]=kernelTrans(self.X,self.X[i,:],kTup)
def calcEk(oS,k):
    fXk=float(multiply(oS.alphas,oS.labelMat).T*oS.k[:,k]+oS.b)
    Ek=fXk-float(oS.labelMat[k])
    return Ek
#用于选择第二个alpha（内循环的启发式方法）
def selectJ(i,oS,Ei):
    maxK=-1;maxDeltaE=0;Ej=0
    oS.eCache[i]=[1,Ei]
    validEcacheList=nonzero(oS.eCache[:,0].A)[0]#Return the indices of the elements that are non-zero.
    if (len(validEcacheList))>1:
        for k in validEcacheList:
            if k==i: continue
            Ek=calcEk(oS,k)
            deltaE=abs(Ei-Ek)
            if(deltaE>maxDeltaE):
                maxK=k;maxDeltaE=deltaE;Ej=Ek
        return maxK,Ej #循环选择其中使得改变最大的那个值
    else:
        j=selectJrand(i,oS.m)
        Ej=calcEk(oS,j)
        return j,Ej
def updateEk(oS,k):
    Ek=calcEk(oS,k)
    oS.eCache[k]=[1,Ek]
# platt SMO 算法优化
def innerL(i,oS):
    Ei=calcEk(oS,i)
    if((oS.labelMat[i]*Ei<-oS.tol)and(oS.alphas[i]<oS.C))or((oS.labelMat[i]*Ei>oS.tol)and(oS.alphas[i]>0)):
        j,Ej=selectJ(i,oS,Ei)
        alphaIold=oS.alphas[i].copy();alphaJold=oS.alphas[j].copy()
        if(oS.labelMat[i]!=oS.labelMat[j]):
            L=max(0,oS.alphas[j]-oS.alphas[i])
            H=min(oS.C,oS.C+oS.alphas[j]-oS.alphas[i])
        else:
            L=max(0,oS.alphas[j]+oS.alphas[i]-oS.C)
            H=min(oS.C,oS.alphas[j]+oS.alphas[i])
        if L==H:print "L==H";return 0
        eta=2.0*oS.k[i,j]-oS.k[i,i]-oS.k[j,j]
        if eta>=0:print "eta>=0";return 0
        oS.alphas[j]-=oS.labelMat[j]*(Ei-Ej)/eta
        oS.alphas[j]=clipAlpha(oS.alphas[j],H,L)
        #更新误差缓存
        updateEk(oS,j)
        if(abs(oS.alphas[j]-alphaJold)<0.00001):
            print"j not moving enough";return 0
        oS.alphas[i]+=oS.labelMat[j]*oS.labelMat[i]*(alphaJold-oS.alphas[j])
        updateEk(oS,i)
        b1=oS.b-Ei-oS.labelMat[i]*(oS.alphas[i]-alphaIold)*oS.k[i,i]-oS.labelMat[j]*(oS.alphas[j]-alphaJold)*oS.k[i,j]
        b2=oS.b-Ej-oS.labelMat[i]*(oS.alphas[i]-alphaIold)*oS.k[i,j]-oS.labelMat[j]*(oS.alphas[j]-alphaJold)*oS.k[j,j]
        if(0<oS.alphas[i])and(oS.C>oS.alphas[i]):oS.b=b1
        elif(0<oS.alphas[j])and(oS.C>oS.alphas[j]):oS.b=b2
        else:oS.b=(b1+b2)/2.0
        return 1
    else:
        return 0
def smoP(dataMatIn,classLabels,C,toler,maxIter,KTup=('lin',0)):
    oS=optStruct(mat(dataMatIn),mat(classLabels).transpose(),C,toler,KTup)
    iter=0
    entireSet=True;alphaPairsChanged=0
    while(iter<maxIter)and((alphaPairsChanged>0)or(entireSet)):
        alphaPairsChanged=0
        if entireSet:
            for i in range(oS.m):
                alphaPairsChanged+=innerL(i,oS)
            print("fullSet,iter:%d i:%d,pairs changed %d"%(iter,i,alphaPairsChanged))
            iter+=1
        else:
            nonBoundIs=nonzero((oS.alphas.A>0)*(oS.alphas.A<C))[0]#遍历所有非边界值
            for i in nonBoundIs:
                alphaPairsChanged+=innerL(i,oS)
                print("non-bounds,iter:%d i:%d,pairs changed %d"%(iter,i,alphaPairsChanged))
            iter+=1
        if entireSet:entireSet=False
        elif (alphaPairsChanged==0):entireSet=True
        print("iteration number:%d"%iter)
    return oS.b,oS.alphas
def calcWs(alphas,dataArr,classLabels):
    X=mat(dataArr);labelMat=mat(classLabels).transpose()
    m,n=shape(X)
    w=zeros((n,1))
    for i in range(m):
        w+=multiply(alphas[i]*labelMat[i],X[i,:].T)
    return w
def kernelTrans(X,A,kTup):
    m,n=shape(X)
    k=mat(zeros((m,1)))
    if kTup[0]=='lin':k=X*A.T
    elif kTup[0]=='rbf':
        for j in range(m):
            deltaRow=X[j,:]-A
            k[j]=deltaRow*deltaRow.T
        k=exp(k/(-1*kTup[1]**2))
    else:
        raise NameError('Houston we have a problem--That Kernel is not recognized')
    return k
def testRbf(k1=1.3):
    dataArr,labelArr=loadDataSet('C:\Users\YAN\Desktop\SVM/testSetRBF.txt')
    b,alphas=smoP(dataArr,labelArr,200,0.0001,10000,('rbf',k1))
    datMat=mat(dataArr);labelMat=mat(labelArr).transpose()
    svInd=nonzero(alphas.A>0)[0]
    '''nonzero(a) 将对矩阵a的所有非零元素， 分别安装两个维度，
一次返回其在各维度上的目录值。如果 a=mat([ [1,0,0],[0,0,0],[0,0,0]])
则 nonzero(a) 返回值为(array([0]), array([0])) , 因为矩阵a只有一个非零值，
在第0行， 第0列。如果 a=mat([ [1,0,0],[1,0,0],[0,0,0]])则 nonzero(a) 返回值为(array([0, 1]), array([0, 0]))
因为矩阵a只有两个非零值， 在第0行、第0列，和第1行、第0列。所以结果元组中，第一个行维度数据为（0,1） 元组第二个列维度都为（0,0）。
'''
    sVs=datMat[svInd]
    labelSV=labelMat[svInd]
    print("there are %d Support vectors"%shape(sVs)[0])
    m,n=shape(datMat)
    errorCount=0
    for i in range(m):
        kernelEval=kernelTrans(sVs,datMat[i,:],('rbf',k1))
        predict=kernelEval.T*multiply(labelSV,alphas[svInd])+b
        if sign(predict)!=sign(labelArr[i]):errorCount+=1
    print("the training error rate is:%f"%(float(errorCount)/m))
    dataArr,labelArr=loadDataSet('C:\Users\YAN\Desktop\SVM/testSetRBF2.txt')
    errorCount=0
    datMat=mat(dataArr);labelMat=mat(labelArr).transpose()
    m,n=shape(datMat)
    for i in range(m):
        kernelEval=kernelTrans(sVs,datMat[i,:],('rbf',k1))
        predict=kernelEval.T*multiply(labelSV,alphas[svInd])+b
        if sign(predict)!=sign(labelArr[i]):errorCount+=1
    print("the testing error rate is:%f"%(float(errorCount)/m))
#################################################    
#                       手写字识别                #
def img2vector(filename):
    returnVect=zeros((1,1024))
    fr=open(filename)
    for i in range(32):
        linestr=fr.readline()
        for j in range(32):
            returnVect[0,32*i+j]=int(linestr[j])
    return returnVect
def loadImages(dirName):
    from os import listdir #目录必备
    hwLabels=[]
    trainingFileList=listdir(dirName)
    m=len(trainingFileList)
    trainingMat=zeros((m,1024))
    for i in range(m):
        fileNameStr=trainingFileList[i]
        fileStr=fileNameStr.split('.')[0]
        classNumStr=int(fileStr.split('_')[0])
        if classNumStr==9:hwLabels.append(-1)
        else:hwLabels.append(1)
        trainingMat[i,:]=img2vector('%s/%s'%(dirName,fileNameStr))#"/"取文件夹中的文件
    return trainingMat,hwLabels
def testDigits(kTup=('rbf',10)):
    dataArr,labelArr=loadImages("trainingDigits")
    b,alphas=smoP(dataArr,labelArr,200,0.0001,1000,kTup)
    datMat=mat(dataArr);labelMat=mat(labelArr).transpose()
    svInd=nonzero(alphas.A>0)[0]
    sVs=datMat[svInd]
    labelSV=labelMat[svInd]
    print"there are %d Support vectors"%shape(sVs)[0]
    m,n=shape(datMat)
    errorCount=0
    for i in range(m):
        kernelEval=kernelTrans(sVs,datMat[i,:],kTup)
        predict=kernelEval.T*multiply(labelSV,alphas[svInd])+b
        if sign(predict)!=sign(labelArr[i]):errorCount+=1
    print("the training error rate is: %f"%(float(errorCount)/m))
    dataArr,labelArr=loadImages('testDigits')
    errorCount=0
    datMat=mat(dataArr)
    m,n=shape(datMat)
    for i in range(m):
        kernelEval=kernelTrans(sVs,datMat[i,:],kTup)
        predict=kernelEval.T*multiply(labelSV,alphas[svInd])+b
        if sign(predict)!=sign(labelArr[i]):errorCount+=1
    print("the testing error rate is: %f"%(float(errorCount)/m))
    
    

    
    
                
    

