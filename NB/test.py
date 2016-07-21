# This Python file uses the following encoding: utf-8
import os, sys
reload(bayes)
listOPosts,listClasses=bayes.loadDataSet()
myVocabList=bayes.createVocabList(listOPosts)
print myVocabList
'''
print bayes.setOfWord2Vec(myVocabList,listOPosts[0])
print bayes.setOfWord2Vec(myVocabList,listOPosts[3])
'''
trainMat=[]
'''
for postinDoc in listOPosts:
    trainMat.append(bayes.setOfWord2Vec(myVocabList,postinDoc))
    p0V,p1V,pAb=bayes.trainNB0(trainMat,listClasses)

print ("非侮辱性元素概率：%s"%p1V)
print ("侮辱性元素概率： %s"%p0V)
print ("侮辱性语言概率：%s"%pAb)
'''
'''
for postinDoc in listOPosts:
    trainMat.append(bayes.setOfWord2Vec(myVocabList,postinDoc))
    p0V,p1V,pAb=bayes.trainNB1(trainMat,listClasses)

print ("非侮辱性元素概率：%s"%p1V)
print ("侮辱性元素概率： %s"%p0V)
print ("侮辱性语言概率：%s"%pAb)
'''
'''
bayes.testingNB()
'''
#bayes.spamTest()
import feedparser
ny=feedparser.parse("http://newyork.craigslist.org/stp/index.rss")
sf=feedparser.parse('http://sfbay.craigslist.org/stp/index.rss')
print bayes.localWords(ny,sf)
bayes.getTopWords(ny,sf)




