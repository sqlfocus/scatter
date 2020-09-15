#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import aiohttp        #pip3 install aiohttp
import asyncio
import json
import time

ret_cnt = 0
async def get_baidu(sess):
    async with sess.get("http://www.baidu.com") as resp:
        if resp.status != 200:
            print("get baidu fail/{}".format(resp.status))
        else:
            await resp.text(encoding="utf-8")
            
            global ret_cnt
            ret_cnt = ret_cnt + 1
            
async def post_baidu(sess):
    async with sess.post("http://www.baidu.com", data=json.dumps({"test":"hello"})) as resp:
        if resp.status != 200:
            print("get baidu fail/{}".format(resp.status))
        else:
            global ret_cnt
            ret_cnt = ret_cnt + 1
        
async def main():
    session = aiohttp.ClientSession()
    pending = set()

    print("begin at: {}".format(time.time()))
    send_cnt = 0
    while True:
        if send_cnt > 5:
            break

        task = asyncio.create_task(get_baidu(session))
        pending.add(task)
        send_cnt = send_cnt + 1
        
        try:
            done, pending = await asyncio.wait(
                pending,
                timeout=0.0001,     #timeout 0.0001s
                return_when=asyncio.FIRST_COMPLETED)
        except asyncio.TimeoutError:
            ###<TK!!!>"asyncio.wait" NOT raise asyncio.TimeoutError
            ###       Futures or Tasks that aren’t done when the timeout
            ###       occurs are simply returned in the second set('pending'
            ###       in this example) ===> SO, NO PRINT
            print("WARN: timeout when get baidu")

    print("pending: {}/{}".format(len(pending), time.time()))
    await asyncio.wait(
        pending,
        return_when=asyncio.ALL_COMPLETED)
    print("end at: {}".format(time.time()))
    print("have sended: {}".format(send_cnt))
    print("have received: {}".format(ret_cnt))

    ###process exit
    await session.close()

if __name__ == "__main__":
    asyncio.run(main())

