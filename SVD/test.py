import svdRec
reload(svdRec)
from numpy import *
'''
Data=svdRec.loadExData()
U,Sigma,VT=linalg.svd(Data)
print Sigma
'''
myMat=mat(svdRec.loadExData())
'''
print svdRec.eulidSim(myMat[:,0],myMat[:,4])
print svdRec.cosSim(myMat[:,0],myMat[:,4])
print svdRec.pearsSim(myMat[:,0],myMat[:,4])
'''
myMat[0,1]=myMat[0,0]=myMat[1,0]=myMat[2,0]=4
'''
print myMat
print(svdRec.recommend(myMat,2))
print (svdRec.recommend(myMat,2,simMeas=svdRec.eulidSim))
print (svdRec.recommend(myMat,2,simMeas=svdRec.pearsSim))
'''
'''
print(svdRec.recommend(myMat,1,estMethod=svdRec.svdEst))
print (svdRec.recommend(myMat,1,estMethod=svdRec.svdEst,simMeas=svdRec.pearsSim))
'''
svdRec.imgCompress(2)











