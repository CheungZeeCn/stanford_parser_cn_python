#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# by zhangzhi @2013-11-05 13:47:04 
# Copyright 2013 NONE rights reserved.
import pickle
"""
sprRecs: structure,
[
[[tag:int, data:'unicode'], [tag:int, data:'unicode'],[tag:int, data:'unicode'],],# person1  
[[tag:int, data:'unicode'], [tag:int, data:'unicode'],[tag:int, data:'unicode'],],# person2
[[tag:int, data:'unicode'], [tag:int, data:'unicode'],[tag:int, data:'unicode'],],# person3
[[tag:int, data:'unicode'], [tag:int, data:'unicode'],[tag:int, data:'unicode'],],# person4
]
"""

if __name__ == '__main__':
    sprRecs = pickle.load(open('dump.pickle', 'r'))
    cntTime = 0
    cntAll = 0
    for spr in sprRecs:
        haveTime = False
        for tag, data in spr:
            if int(tag)  == 132:
                haveTime = True
                print data.encode('UTF-8'),
            if int(tag) in (152, ) or data.strip() == '；'.decode('UTF-8') or \
                data.strip() == '！'.decode('UTF-8'):
                print "\n",
        if haveTime == True:
            cntTime += 1
        cntAll += 1
        print "\n\n############################\n\n"
    print "#statistic: #rec:[%d] recWithTime:[%d] rate:[%.4f]" % (cntAll, cntTime, cntTime*1.0/cntAll)
