# -*- coding: utf-8 -*-
import json

data = json.load(open('G:/virtualenv/gaohu/gaohu/app/followers.json'))
for i in data:
    print i ,data[i]