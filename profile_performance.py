#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

'''
利用cProfile模块查看函数耗时，并按照耗时排序
  python3 -m cProfile -o perf.out profile_performance.py
  python3 -c "import pstats; p=pstats.Stats('perf.out'); p.sort_stats('time').print_stats()"

现实信息各字段含义
  ncalls：表示函数调用的次数
  tottime：表示指定函数的总的运行时间，除掉函数中调用子函数的运行时间
  percall：（第一个percall）等于 tottime/ncalls
  cumtime：表示该函数及其所有子函数的调用运行的时间，即函数开始调用到返回的时间
  percall：（第二个percall）即函数运行一次的平均时间，等于 cumtime/ncalls
  filename:lineno(function)：每个函数调用的具体信息

按照函数名排序，只打印前3行函数的信息
  p.strip_dirs().sort_stats("name").print_stats(3)
按照运行时间和函数名进行排序，打印前百分之几的函数信息
  p.strip_dirs().sort_stats("cumulative", "name").print_stats(0.8)
有哪些函数调用了bar
  p.print_callers("bar")
查看test()函数中调用了哪些函数
  p.print_callees("foo")
'''

def func1():
    sum = 0
    for i in range(1000000):
        sum += i
        
def func2():
    time.sleep(10)

func1()
func2()
