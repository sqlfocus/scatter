#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import time

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)
    
async def run_task_sync():
    print("\nrun task sync")
    
    print(f"started at {time.strftime('%X')}")
    await say_after(1, 'sleep 1')
    await say_after(2, 'sleep 2')
    print(f"finished at {time.strftime('%X')}")

async def run_task_concurrent_format1():
    print("\ncreate task, and run concurrent")
    task1 = asyncio.create_task(say_after(1, 'sleep 1'))
    task2 = asyncio.create_task(say_after(2, 'sleep 2'))

    print(f"started at {time.strftime('%X')}")
    await task1
    await task2
    print(f"finished at {time.strftime('%X')}")

async def run_task_concurrent_format2():
    print("\ngather task, and run concurrent")
    
    print(f"started at {time.strftime('%X')}")
    await asyncio.gather(
        say_after(1, "sleep 1"),
        say_after(2, "sleep 2"),
    )
    print(f"finished at {time.strftime('%X')}")
    
async def wait_task_timeout():
    print("\nwait task finish, by timeout")
    # Wait for at most 1 second
    try:
        await asyncio.wait_for(say_after(3, "should not appear"), timeout=1.0)
    except asyncio.TimeoutError:
        print('timeout!')

async def wait_task_only_one_complete():
    print("\nwait one task complete")

    try:
        task_sleep_2 = asyncio.create_task(say_after(2, "sleep 2"))
        task_sleep_1 = asyncio.create_task(say_after(1, "sleep 1"))
        task_sleep_3 = asyncio.create_task(say_after(3, "sleep 3"))
        task_sleep_1.add_done_callback(lambda res: print("done task_sleep_1"))
        
        done, pending = await asyncio.wait(
            {task_sleep_2, task_sleep_1, task_sleep_3},
            timeout=5,
            return_when=asyncio.FIRST_COMPLETED)  #FIRST_EXCEPTION/ALL_COMPLETED
        if task_sleep_1 in done:
            print("task_sleep_1 in done")
        for task in pending:
            task.cancel()
        try:
            for task in pending:
                await task
        except asyncio.CancelledError:
            print("have canceled, should NOT await")
    except asyncio.TimeoutError:
        print('timeout!')

        
        
if __name__ == "__main__":
    asyncio.run(wait_task_only_one_complete())
    asyncio.run(wait_task_timeout())
    asyncio.run(run_task_concurrent_format2())
    asyncio.run(run_task_concurrent_format1())
    asyncio.run(run_task_sync())


