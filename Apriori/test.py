# This Python file uses the following encoding: utf-8
import os, sys
import apriori
reload(apriori)
dataSet=apriori.loadDataSet()
'''
print dataSet
C1=apriori.createC1(dataSet)
print C1
D=map(set,dataSet)
print D
L1,suppData0=apriori.scanD(D,C1,0.5)
print L1
print suppData0
'''
'''
L,suppData=apriori.apriori(dataSet)
print L
print suppData
'''
'''
L1,suppData1=apriori.apriori(dataSet,minSupport=0.7)
print L1
print suppData1
'''
'''
L,suppData=apriori.apriori(dataSet,minSupport=0.5)
rules=apriori.generateRules(L,suppData,minConf=0.7)
print rules
rules=apriori.generateRules(L,suppData,minConf=0.5)
print rules
'''
'''
#--------------国会投票------------#
actionIdList,billTitles=apriori.getActionIds()
'''
mushDatSet=[line.split() for line in open("C:\Users\YAN\Desktop\Apriori/mushroom.dat").readlines()]
L,suppData=apriori.apriori(mushDatSet,minSupport=0.3)
for item in L[1]:
    #intersection 表示交集的意思
    if item.intersection('2'):
        print item


























