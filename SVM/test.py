import svmMLiA
reload(svmMLiA)
dataArr,labelArr=svmMLiA.loadDataSet('C:\Users\YAN\Desktop\SVM/testSet.txt')
#print labelArr
#b,alphas=svmMLiA.smoSimple(dataArr,labelArr,0.6,0.001,40)
'''
b,alphas=svmMLiA.smoP(dataArr,labelArr,0.6,0.001,40)
print ("b is %d"%b)
print("the number of alphas(>0):",alphas[alphas>0])
for i in range(100):
    if alphas[i]>0.0:
        print dataArr[i],labelArr[i]
ws=svmMLiA.calcWs(alphas,dataArr,labelArr)
print ("W is:",ws)
'''
#svmMLiA.testRbf()
svmMLiA.testDigits(('rbf',20))

