#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import multiprocessing
import sys
import threading
import time

'''
Python线程虽然是真正的线程，但解释器执行代码时，必须获得GIL锁,
Global Interpreter Lock；这导致所有线程实际上串行运行，并没有
并行效果
'''

__CPUS = multiprocessing.cpu_count()
if __CPUS <=1:
    sys.exit(-1)

    
class StoppableThread(threading.Thread):
    '''
    thread with a stop() method
    '''
    def __init__(self, func, arg):
        '''
        param func [func point] function that will be called repeatedly
        '''
        super(StoppableThread, self).__init__()
        self._stop_event = threading.Event()
        self._func = func
        self._arg = arg
        
    def stop(self):
        self._stop_event.set()
    def stopped(self):
        return self._stop_event.is_set()
    
    def run(self):
        while not self.stopped():
            self._func(self._arg)

            
def test_loop(id):
    '''
    thread loop func, will be called again and again
    '''
    time.sleep(1)       #sleep 1s
    print("in thread: ", id)
            
def main():
    threads = []

    #create
    for i in range(__CPUS-1):
        t = StoppableThread(test_loop, i)
        t.setDaemon(True)
        threads.append(t)
        
    #start
    for t in threads:
        t.start()

    #sleep to wait thread
    time.sleep(10)
    
    #stop
    for t in threads:
        t.stop()
    for t in threads:
        t.join()
            
if __name__ == "__main__":
    sys.exit(main())
