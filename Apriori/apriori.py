# This Python file uses the following encoding: utf-8
import os, sys
def loadDataSet():
    return [[1,3,4],[2,3,5],[1,2,3,5],[2,5]]
#创建只有一个元素的集合
def createC1(dataSet):
    C1=[]
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    #对C1中的每个项构建一个不变的集合
    return map(frozenset,C1)
#创建频繁项集
def scanD(D,Ck,minSupport):
    #D数据集，Ck候选集，minSupport最小支持度
    ssCnt={}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                #判断候选集中的元素是否是数据集的子集
                if not ssCnt.has_key(can):ssCnt[can]=1
                else: ssCnt[can]+=1
    numItems=float(len(D))
    retList=[]
    supportData={}
    for key in ssCnt:
        support=ssCnt[key]/numItems
        if support>=minSupport:
            retList.insert(0,key)#在第一行插入数据
        supportData[key]=support
    return retList,supportData
#-------生成大小为k的候选集---------#
def aprioriGen(Lk,k):
    #创建候选项集
    retList=[]
    lenLk=len(Lk)
    for i in range(lenLk):
        for j in range(i+1,lenLk):
            L1=list(Lk[i])[:k-2];L2=list(Lk[j])[:k-2]
            #比较list表前k-2个元素，相等时合并两者后变成大小为k的list
            L1.sort();L2.sort()
            if L1==L2:
                retList.append(Lk[i]|Lk[j])
    return retList
#--------------Apriori----------------#
def apriori(dataSet,minSupport=0.5):
    C1=createC1(dataSet)
    D=map(set,dataSet)
    L1,supportData=scanD(D,C1,minSupport)
    L=[L1]#每个不同的K对应不同的集合
    k=2
    while(len(L[k-2])>0):
        Ck=aprioriGen(L[k-2],k)
        Lk,supK=scanD(D,Ck,minSupport)
        supportData.update(supK)
        L.append(Lk)
        k+=1
    return L,supportData
#------------对规则进行评估---------------#
def calcConf(freqSet,H,supportData,br1,minConf=0.7):
    prunedH=[]
    for conseq in H:
        conf=supportData[freqSet]/supportData[freqSet-conseq]
        if conf>=minConf:
            print freqSet-conseq,"--->",conseq,"conf:",conf
            br1.append((freqSet-conseq,conseq,conf))
            prunedH.append(conseq)
    return prunedH
#---------------生成候选规则集合---------#
def rulesFromConseq(freqSet,H,supportData,br1,minConf=0.7):
    m=len(H[0])
    #尝试进一步合并
    if(len(freqSet)>(m+1)):
        Hmp1=aprioriGen(H,m+1)
        #创建Hm+1的候选集
        Hmp1=calcConf(freqSet,Hmp1,supportData,br1,minConf)
        if(len(Hmp1)>1):
            rulesFromConseq(freqSet,Hmp1,supportData,br1,minConf)
def generateRules(L,supportData,minConf=0.7):
    bigRuleList=[]
    for i in range(1,len(L)):
        for freqSet in L[i]:
            H1=[frozenset([item]) for item in freqSet]
            if(i>1):
                rulesFromConseq(freqSet,H1,supportData,bigRuleList,minConf)
            else:
                calcConf(freqSet,H1,supportData,bigRuleList,minConf)
            
    return bigRuleList
from time import sleep
from votesmart import votesmart
votesmart.apikey='49024thereoncewasamanfromnantucket94040'
def getActionIds():
    actionIdList=[];billTitleList=[]
    fr=open('C:\Users\YAN\Desktop\Apriori/recent20bills.txt')
    for line in fr.readlines():
        billNum=int(line.split('\t')[0])
        try:
            billDetail=votesmart.votes.getBill(billNum)
            for action in billDetail.actions:
                if action.level=='House'and(action.stage=='Passage'or\
                                          action.stage=='Amendment Vote'):
                    actionId=int(action.actionId)
                    print("bill:%d has actionId:%d"%(billNum,actionId))
                    actionIdList.append(actionId)
                    billTitleList.append(line.strip().split('\t')[1])
        except:
            print"problem getting bill %d"%billNum
        sleep(1)
    return actionIdList,billTitleList
#----------------基于投票数据的事务列表填充函数------------#
def getTransList(actionIdList,billTitleList):
    itemMeaning=['Republican','Democratic']
    for billTitle in billTitleList:
        itemMeaning.append("%s--Nay"%billTitle)
        itemMeaning.append("%s--Yea"%billTitle)
    transDict={}
    voteCount=2
    for actionId in actionIdList:
        sleep(3)
        print"getting votes for actionId:%d"%actionId
        try:
            voteList=votesmart.votes.getBillActionVotes(actionId)
            for vote in voteList:
                if not transDict.has_key(vote.candidateName):
                    transDict[vote.candidateName]=[]
                    if vote.officeParties=="Democratic":
                        transDict[vote.candidateName].append(1)
                    elif vote.officeParties=="Republican":
                        transDict[vote.candidateName].append(0)
                if vote.action=="Nay":
                    transDict[vote.candidateName].append(voteCount)
                elif vote.action=="Yea":
                    transDict[vote.candidateName].append(voteCount+1)
        except:
            print"problem getting actionId:%d"%actionId
        voteCount+=2
    return transDict,itemMeaning

























    








































    
