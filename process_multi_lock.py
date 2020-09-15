#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from multiprocessing import Process, Lock

def f(l, i):
    l.acquire()
    try:
        print('hello world', i)
    finally:
        l.release()
        pass

if __name__ == '__main__':
    lock = Lock()

    procs = []
    for num in range(10):
        procs.append(Process(target=f, args=(lock, num)))

    for p in procs:
        p.start()
    for p in procs:
        p.join()
