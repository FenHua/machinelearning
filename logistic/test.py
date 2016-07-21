import logRegres
from numpy import *
reload(logRegres)

#dataArr,labelMat=logRegres.loadDataSet()
#weights=logRegres.gradAscent(dataArr,labelMat)
#w=logRegres.stocGradAscent0(array(dataArr),labelMat)
'''
w=logRegres.stocGradAscent1(array(dataArr),labelMat,500)
print w
logRegres.plotBestFit(w)
'''
logRegres.multiTest()
