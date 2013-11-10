#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# by zhangzhi @2013-11-09 21:10:15 
# Copyright 2013 NONE rights reserved.

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

if __name__ == '__main__':
    print combineSameTag([('1', '2'), ('1', '2'), ('2', '3'), ('2', '2'), ('2', '3')])
