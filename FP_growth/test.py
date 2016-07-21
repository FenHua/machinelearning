# This Python file uses the following encoding: utf-8
import os, sys
import fbGrowth
'''
rootNode=fbGrowth.treeNode('pyramid',9,None)
rootNode.children['eye']=fbGrowth.treeNode('eye',13,None)
rootNode.children['phoenix']=fbGrowth.treeNode('phoenix',3,None)
rootNode.disp()
'''
reload(fbGrowth)
'''
simpDat=fbGrowth.loadSimpDat()
initSet=fbGrowth.createInitSet(simpDat)
print initSet
myFPtree,myHeaderTab=fbGrowth.createTree(initSet,3)
'''
'''
myFPtree.disp()
print fbGrowth.findPrefixPath('x',myHeaderTab['x'][1])
print fbGrowth.findPrefixPath('z',myHeaderTab['z'][1])
print fbGrowth.findPrefixPath('r',myHeaderTab['r'][1])
'''
'''
freqItems=[]
fbGrowth.minTree(myFPtree,myHeaderTab,3,set([]),freqItems)
'''
parsedDat=[line.split() for line in open("C:\Users\YAN\Desktop\FP_growth/kosarak.dat").readlines()]
initSet=fbGrowth.createInitSet(parsedDat)
myFPtree,myHeaderTab=fbGrowth.createTree(initSet,100000)
myFreqList=[]
fbGrowth.minTree(myFPtree,myHeaderTab,100000,set([]),myFreqList)
print len(myFreqList)
print myFreqList




















