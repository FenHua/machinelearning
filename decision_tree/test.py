'''
reload(tree)
myDat,labels=tree.createDataSet()
print myDat
print labels
'''
'''
print tree.calcShannonEnt(myDat)
myDat[0][-1]='maybe'
print myDat
print tree.calcShannonEnt(myDat)
'''
'''
print tree.splitDataSet(myDat,0,1)
print tree.splitDataSet(myDat,0,0)
print tree.chooseBestFeatureToSplit(myDat)
myTree=tree.createTree(myDat,labels)
print myTree
'''
'''
import treePlotter
reload(treePlotter)
print treePlotter.retrieveTree(1)
myTree=treePlotter.retrieveTree(0)
print treePlotter.getNumLeafs(myTree)
print treePlotter.getTreeDepth(myTree)
print treePlotter.createPlot(myTree)
'''
import tree
reload(tree)
'''
myDat,labels=tree.createDataSet()
print labels
myTree=treePlotter.retrieveTree(0)
print myTree
print tree.classify(myTree,labels,[1,0])
print tree.classify(myTree,labels,[1,1])
tree.storeTree(myTree,'classfierStorage.txt')
print tree.grabTree('classfierStorage.txt')
'''
fr=open('lenses.txt')
lenses=[inst.strip().split('\t') for inst in fr.readlines()]
lensesLabels=['age','prescript','astigmatic','tearRate']
lensesTree=tree.createTree(lenses,lensesLabels)
print lenses
import treePlotter
treePlotter.createPlot(lenseTree)