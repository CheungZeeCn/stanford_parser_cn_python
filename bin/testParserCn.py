#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# by zhangzhi @2013-11-08 19:16:28 
# Copyright 2013 NONE rights reserved.
import stanfordParserPipeCn as P
import nltk 

def traverse(t):
    try:
        t.node
    except AttributeError:
        "one leaf is here"
        print "Error"
        print t,
    else:
        # Now we know that t.node is defined
        print '(', t.node,
        print "========="
        for child in t:
            print "child"
            traverse(child)
        print ')',

if __name__ == '__main__':
    #ret = P.parse("张智 于 2010 年 于 哈尔滨 工业 大学 毕业 ， 毕业 后 在 百度 工作 至 2013 年 。")
    ret = P.parse("The dog find the god")
    #print ret[1]
    t = nltk.Tree.parse(ret[1])
    t.draw()
    traverse(t)



