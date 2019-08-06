#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import urllib.request

def get():
    try:
        req = urllib.request.Request("http://www.baidu.com/")
        res = urllib.request.urlopen(req)
        print(res.read().decode('utf-8'))
    except Exception as err:
        print("get err: {}".format(err))
    
def post():
    try:
        req = urllib.request.Request(
            "http://zookeeper.apache.org",
            data=json.dumps({"test":1, "hello":"world"}).encode('utf-8'),
            method='POST'
        )
        res = urllib.request.urlopen(req)
        print(res.read().decode('utf-8'))
    except Exception as err:
        print("post err: {}".format(err))


def delete():
    try:
        args = "id={}&domain={}&sub_domain={}".format(
            1, "test", "subtest"
        )
        req = urllib.request.Request(
            "http://zookeeper.apache.org/" + args,
            method='DELETE'
        )
        res = urllib.request.urlopen(req)
        print(res.read().decode('utf-8'))
    except Exception as err:
        print("delete err: {}".format(err))


if __name__ == "__main__":
    get()
    post()
    delete()
