#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# by zhangzhi @2013-11-09 10:10:51 
# Copyright 2013 NONE rights reserved.

import readDb as R
import stanfordParserPipeCn as P
import logging
import nltk 
import sys

def seperateTag(dataList):
    sprData = []
    for i in range(0, len(dataList), 2):
        sprData.append([int(dataList[i+1]), dataList[i]])
    return sprData

def seperateSent(tagSprData):
    sentList = []
    aSent = []
    for each in tagSprData:
        aSent.append(each)
        tag, data = each
        if int(tag) in (152, ) \
            or \
            data.strip() == '；'.decode('UTF-8') \
            or \
            data.strip() == '！'.decode('UTF-8'):
            sentList.append(aSent)
            aSent = []
    if aSent != []:
        sentList.append(aSent)
    return sentList      

def sprData(recs):
    sprRecs = {}
    for rec in recs:
        pid = int(rec['pid'])
        data = rec['introductionSeg'].strip()
        dataList = data.split("\t")
        try:
            sprData = seperateTag(dataList)
            sprData = seperateSent(sprData)
            #debug
            #sprData = sprData[0:2]
        except Exception, e:
            logging.error("%s|datalist:[%s]" % (e, dataList))
            sprData = []
        sprRecs[pid] = sprData
    return sprRecs

def ppList(l):
    print "[" 
    for each in l:
        if type(each) == tuple or type(each) == list:
            ppList(each)
        else:
            print each,
    print "]" 

def combineTuple(redundantTuples):
    """
        flat the redundantTuples in to list of tuples
        |time|company|department|position|
    """
    ret = []
    rt = redundantTuples
    #print "rt====" * 10
    #ppList(rt)
    #print "rt====end" * 10
    if rt[0] != []:
        time = " # ".join(rt[0])
    else:
        time = None
    # redundant fields: company|department|position
    for i in range(1, 4):
        if len(rt[i]) == 0:
            rt[i] = [None]
    for c in rt[1]:  
        for d in rt[2]:
            for p in rt[3]:
                #print time, c,d,p
                ret.append([time, c, d, p])
    print "combine====================="
    for oneTuples in ret:
        for i in range(len(oneTuples)):
            if oneTuples[i] == None:
                oneTuples[i] = 'None'
            else:
                oneTuples[i] = oneTuples[i].encode('utf-8')
        print " | ".join(oneTuples)
    print "combine=====================END"
    return ret

# for every Sent, we have a g_retTupleList
# for every IP, we add an item in the list
# this item is a list
# with the struct of [time, company, department position]
g_retTupleList = []

def traverse(t, sent, sentPos=0):
    """
    traverse the tree and the sent to collect the 
    tuples into g_retTupleList
    for every child sent noded by IP,
    we collect the tuples, add it into g_retTupleList
    """
    global g_retTupleList
    try:
        t.node
    except AttributeError:# a leaf
        #one leaf is here
        #t is the string data, sent[sentPos] is the sent data
        if len(g_retTupleList) == 0: #do not thing
            pass  
        else:
            tag = sent[sentPos][0]
            word = sent[sentPos][1]
            #print tag, type(tag), word
            if tag == 132: #time
                #print 'g_retTupleList'
                #ppList(g_retTupleList)
                #print 132, word
                (g_retTupleList[-1][0]).append(word)
                #print 'g_retTupleList'
                #ppList(g_retTupleList)
            elif tag == 888: #company
                #print 888, word
                (g_retTupleList[-1][1]).append(word)
            elif tag == 777: #department
                #print 777, word
                (g_retTupleList[-1][2]).append(word)
            elif tag == 999: #position
                #print 'g_retTupleList'
                #ppList(g_retTupleList)
                #print 999, word
                (g_retTupleList[-1][3]).append(word)
                #print 'g_retTupleList'
                #ppList(g_retTupleList)
            else:
                pass
        sentPos += 1
    else: # an inner node
        # Now we know that t.node is defined
        if t.node == 'IP': #IP~~ new a list
            g_retTupleList.append([[],[],[],[]])
            #debug
            #if len(g_retTupleList) != 0:
            #    print "new IP"
            #    print g_retTupleList
            #    ppList(g_retTupleList)
        for child in t:
            sentPos = traverse(child, sent, sentPos)
    return sentPos

def combineSameTag(sent):
    """for one sentence, combine the words with the say tag"""
    cache = ''
    lastTag = ''
    newSent = []
    for tag, data in sent:
        if tag == lastTag:
            cache += data 
        else: #!=
            if cache != '':
                newSent.append([lastTag, cache])
            lastTag = tag
            cache = data
    newSent.append([lastTag, cache])
    return newSent

def extractOneSent(sent):
    """
        extract one sent, find out the
        |pid|time|company|department|position|
        if they exist in this sentence
    """
    global g_retTupleList
    #clean the cache
    g_retTupleList = []
    #combine wors with the same tag into a word
    sent = combineSameTag(sent)
    #combine the sent into string devided by space
    sentStr = " ".join([ x[1] for x in sent ]) 
    #debug
    print sentStr
    ##print sentStr
    #sentStr = " ".join([ "%s_%s" % (x[1], x[0])  for x in sent ]) 
    #print sentStr
    ret = P.parse(sentStr.encode('utf-8'))
    t = nltk.Tree.parse(ret[1])
    #t.draw()
    # traverse the tree and the sent which will modify the
    # global variable g_retTupleList
    traverse(t, sent)
    # combine the g_retTupleList so that we have the real tuples without \
    # redundants
    retTuples = []
    #debug
    for each in g_retTupleList:
        #print 'each' , each
        #print 'combined', combineTuple(each)
        retTuples += combineTuple(each)
    #print 'ret', retTuples
    return retTuples

def extractOnePerson(sents):
    """extract one person"""
    #init, some register, some flag
    personTuplesList = []
    for sent in sents:
        "tt => [time,company,department,position]"
        retTuples = extractOneSent(sent)
        #print "retTuples", retTuples
        personTuplesList += retTuples
    return personTuplesList

def extractData(recs):
    """extractData into |pid|time|company|department|position|"""
    # tag it
    "sprRecs => { pid: sentences }   sentences => [ sent1, sent2, sent3 ]"
    "sent => [ (tag1, data1), (tag2, data2), (tag3, data3)]" 
    sprRecs = sprData(recs)
    for pid, sents in sprRecs.items():
        ret = extractOnePerson(sents)
        #print ret
        #output 
        for oneTuples in ret:
            oneTuples.insert(0, str(pid))
            #print oneTuples
            #for i in range(len(oneTuples)):
            #    if oneTuples[i] == None:
            #        oneTuples[i] = 'None'
            #    else:
            #        try:
            #            oneTuples[i] = oneTuples[i].encode('utf-8')
            #        except Exception, e:
            #            print "error, %s [%s]" % (e, oneTuples[i])
            #print "|||".join(oneTuples)
    #done

if __name__ == '__main__':
    #init DB
    if R.initDb() != True:
        print "exit"
        sys.exit(-1)    
    #if we have toooo many recs(more than 100K),
    #we may optimise here.
    dbData = R.readData('intro_for_event_extraction', 2)    

    extractData(dbData)
    R.quitDb()
