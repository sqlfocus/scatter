#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import multiprocessing
import sys
import time


__CPUS = multiprocessing.cpu_count()
if __CPUS <=1:
    sys.exit(-1)


class SProc(multiprocessing.Process):
    def __init__(self, args):
        '''
        param args [dict] dict by shared mem
        '''
        multiprocessing.Process.__init__(self)
        self._dict = args
        self._dict["start"] = int(time.time())

    def run(self):
        print("process[", self._dict.get("id", -1), "] start: ", self._dict.get("start", -1))
        while True:
            time.sleep(1)
            print("in process[", self._dict.get("id", -1), "] run: ", int(time.time() - self._dict.get("start", -1)))

    
def main():
    procs = []
    dicts = []

    #create
    for i in range(__CPUS):
        dt = multiprocessing.Manager().dict()
        dt["id"] = i
        
        p = SProc(dt)
        p.daemon = True
        
        procs.append(p)
        dicts.append(dt)

    #start
    for p in procs:
        p.start()

    #sleep to wait sub process
    time.sleep(3)

    #stop
    for p in procs:
        p.terminate()
    for p in procs:
        p.join()

    #trick
    for dt in dicts:
        print("process[", dt.get("id"), "] start: ", dt.get("start"))

    
if __name__ == "__main__":
    sys.exit(main())
