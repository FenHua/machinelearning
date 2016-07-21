import KNN
reload(KNN)
'''
group,labels=KNN.createDateSet()
print group
print labels
print (KNN.classify0([0,0],group,labels,3))
'''
'''
datingDataMat,datingLabels=KNN.file2matrix('C:\Users\YAN\Desktop\data\datingTestSet2\datingTestSet2.txt')

from numpy import *
import matplotlib
import matplotlib.pyplot as plt
fig=plt.figure()
ax=fig.add_subplot(111)
'''

'''
#scatter(x, y, s=20, c=u'b', marker=u'o', cmap=None, norm=None, vmin=None, vmax=None, alpha=None, linewidths=None, verts=None, hold=None, **kwargs)
ax.scatter(datingDataMat[:,1],datingDataMat[:,2])
'''
'''
ax.scatter(datingDataMat[:,1],datingDataMat[:,2],15.0*array(datingLabels),15.0*array(datingLabels))
plt.show()
'''
'''
normMat,ranges,minVals=KNN.autoNorm(datingDataMat)

KNN.datingClassTest("C:\Users\YAN\Desktop\data\datingTestSet2\datingTestSet2.txt")
'''
testVector=KNN.img2vector("trainingDigits/0_13.txt")
KNN.handwritingClassTest()
