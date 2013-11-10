#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# by zhangzhi @2013-11-08 20:10:03 
# Copyright 2013 NONE rights reserved.
import os
mx = 4000

includes_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stanford-parser')
parser_path = os.path.join(includes_dir,'stanford-parser.jar')
model_path = os.path.join(includes_dir, "edu/stanford/nlp/models/lexparser/chineseFactored.ser.gz")


