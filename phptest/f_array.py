#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys

def aaa():
    u = [1, 2, 3, 4, 5]
    print(u)
    return json.dumps(u)

def f_array():
    r = [0,1]
    f0 = 0
    f1 = 1
    m=5
    for i in range(m):
        f2=f0+f1
        f0=f1
        f1=f2
        r.append(f2)
    print(r)
    return json.dumps(r)
    
if __name__ == '__main__':
    f_array()
