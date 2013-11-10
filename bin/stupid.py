#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# by zhangzhi @2013-11-05 13:18:59 
# Copyright 2013 NONE rights reserved.

import readDb
import pickle
import sys

tbl = 'intro_for_event_extraction'
readDb.initDb()

def seperateTag(dataList):
    sprData = []
    for i in range(0, len(dataList), 2):
        sprData.append([dataList[i+1], dataList[i]])
    return sprData

def test():
    sprRecs = []
    ret = readDb.readData(tbl,)
    for rec in ret:
        pid = int(rec['pid'])
        data = rec['introductionSeg'].strip()
        dataList = data.split("\t")
        sprData = seperateTag(dataList)
        sprRecs.append(sprData) 
    for spr in sprRecs:
        for tag, data in spr:
            print tag, data.encode('UTF8')
    return sprRecs
    

if __name__ == '__main__':
    ret = test()
    sys.exit(-1)
    f = open('dump.pickle', 'w')
    pickle.dump(ret, f)
    f.close()
    
