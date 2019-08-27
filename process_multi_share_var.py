#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import multiprocessing
import sys
import time

###shared dict by multi-process
#<NOTE>ONLY support 'assign oper'/_DICT["xxx"] = xxx_value
#      so if
#        _DICT = {"test":{"val":3, "id":2}}
#      change to
#        _DICT = {"test":{"val":4, "id":2}}
#      MUST by
#        tmp = _DICT.get("test")
#        tmp["val"] = 4
#        _DICT["test"] = tmp
#      If miss '_DICT["test"] = tmp', _DICT.test.val will
#      NOT change, because 'tmp' is JUST local
_DICT = multiprocessing.Manager().dict()

###shared list
_LIST = multiprocessing.Manager().list()

###shared value
#  'c': ctypes.c_char,  'u': ctypes.c_wchar,
#  'b': ctypes.c_byte,  'B': ctypes.c_ubyte,
#  'h': ctypes.c_short, 'H': ctypes.c_ushort,
#  'i': ctypes.c_int,   'I': ctypes.c_uint,
#  'l': ctypes.c_long,  'L': ctypes.c_ulong,
#  'f': ctypes.c_float, 'd': ctypes.c_double
_VALUE_STR = multiprocessing.Manager().Value("c", value="hello, world")
_VALUE_INT = multiprocessing.Manager().Value("d", value=5)
_VALUE_D = multiprocessing.Manager().Value("f", value=5.0)

__CPUS = multiprocessing.cpu_count()
if __CPUS <=1:
    sys.exit(-1)


class SProc(multiprocessing.Process):
    def __init__(self, id):
        '''
        param args [dict] dict by shared mem
        '''
        multiprocessing.Process.__init__(self)
        self._id = str(id)
        _DICT[self._id] = {"start": int(time.time())}
        _LIST.append(self._id)

    def run(self):
        print(_VALUE_STR.value, "/", _VALUE_INT.value, "/", _VALUE_D.value)
        print("process[", self._id, "] start: ", _DICT.get(self._id, {}).get("start"))
        while True:
            time.sleep(1)
            print("in process[", self._id, "] run: ", int(time.time() - _DICT.get(self._id, {}).get("start", -1)))

    
def main():
    procs = []

    #create
    for i in range(__CPUS):
        p = SProc(i)
        p.daemon = True
        procs.append(p)

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
    print(_DICT)
    print(_LIST)
    print(_VALUE_STR.value, "/", _VALUE_INT.value, "/", _VALUE_D.value)

    
if __name__ == "__main__":
    sys.exit(main())
