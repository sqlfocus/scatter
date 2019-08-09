#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

'''
利用cProfile模块查看函数耗时，并按照耗时排序
  python3 -m cProfile -o perf.out profile_performance.py
  python3 -c "import pstats; p=pstats.Stats('perf.out'); p.sort_stats('time').print_stats()"
'''

def func1():
    sum = 0
    for i in range(1000000):
        sum += i
        
def func2():
    time.sleep(10)

func1()
func2()
