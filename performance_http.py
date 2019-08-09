#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Locust（俗称 蝗虫）, 是一个易于使用的，分布式的，用户负载测试工具。
用于web站点（或其他系统）的负载测试，然后算出系统能够处理多少并发
用户。

使用步骤
- 安装: pip install locustio
- 编写locust文件: perf.py
- 执行: locust -f perf.py [--host=http://example.com]
- 打开浏览器, http://127.0.0.1:8089, 输入并发数/增长速率
- 点击Start Swarming
- 查看执行结果

多进程分布式运行
  locust -f perf.py --master [--host=http://test-host]
  locust -f perf.py --slave [--host=http://test-host]

多主机分布式运行
  locust -f perf.py --master [--host=http://test-host]
  locust -f perf.py --slave --master-host=192.168.0.100 [--host=http://test-host]

无web运行
  locust -f perf.py --no-web -c 1000 -r 100 --run-time 1h30m
'''

from locust import HttpLocust,TaskSet,TaskSequence,task,seq_task

class MyTaskSequence(TaskSequence):
    '''
    TaskSequence class is a TaskSet but its tasks will 
    be executed in order
    '''
    def setup(self):
        print("MyTaskSequence setup")
    def teardown(self):
        print("MyTaskSequence teardown")

    def on_start(self):
        print("MyTaskSequence on_start")
    def on_stop(self):
        print("MyTaskSequence on_stop")

        
    @seq_task(1)            #exec order
    def first_task(self):
        print("first_task")

    @seq_task(2)
    def second_task(self):
        print("second_task")

    @seq_task(3)
    @task(2)                #run 2 times
    def third_task(self):
        print("third_task")

    @seq_task(4)
    def stop(self):
        self.interrupt()    #exit 'MyTaskSequence'
    
class UserBehavior(TaskSet):
    '''
    define the user's behaviour, through a collection of tasks

    When a load test is started, each instance of the spawned 
    Locust classes will start executing their TaskSet. What 
    happens then is that each TaskSet will pick one of its tasks
    and call it. It will then wait a number of milliseconds, 
    chosen at random between the Locust class' min_wait and max_wait
    attributes(unless min_wait/max_wait have been defined directly
    under the TaskSet, in which case it will use its own values
    instead). Then it will again pick a new task to be called, 
    wait again, and so on

    <NOTE>self.client, refer 'https://docs.locust.io/en/stable/api.html'
      1. preserve cookies between requests
      2. support 'get', 'post', 'put', 'delete', 'head', 'patch' and 'options'
      3. resp = self.client.post("/login", {"username":"testuser", "password":"secret"})
         resp.status_code: Response status code
         resp.text: Response content

    <NOTE>http client is configured to run in safe_mode. What this does
          is that any request that fails due to a connection error, timeout, 
          or similar will not raise an exception, but rather return an
          empty dummy Response object. The request will be reported as a
          failure in Locust's tatistics. The returned dummy Response's
          content attribute will be set to None, and its status_code will
          be 0.
    '''
    ###nest another TaskSet
    tasks = {MyTaskSequence:1}
    ###another nest format
    #@task
    #class SubTaskSet(TaskSet):
    #    @task
    #    def my_task(self):
    #        pass
    
    #for Locust or TaskSet, run ONLY ONCE
    def setup(self):
        print("UserBehavior setup")
    def teardown(self):
        print("UserBehavior teardown")
    #a simulated user starts/stop executing that TaskSet class
    def on_start(self):
        print("UserBehavior on_start")
    def on_stop(self):
        print("UserBehavior on_stop")

    #declare a task, takes an optional weight argument;
    #in the example, index() will be executed twice as
    #much as version()
    @task(2)
    def index(self):
        with self.client.get("/", catch_response=True) as resp:
            if resp.content == b"":  #set fail by ourself
                resp.failure("Got wrong response")
                
    @task(1)
    def version(self):
        resp = self.client.get("/version")
        print("Response status code:", resp.status_code)
        print("Response content:", resp.text)

class WebsiteUser(HttpLocust):
    '''
    represents a user, Locust will spawn (hatch) one instance of
    the locust class for each user that is being simulated
    '''
    ###<ATTR host>a URL prefix (i.e. https://google.com) to the
    #        host that is to be loaded; Can use the '--host' option
    #        in command line instead
    host = 'https://www.baidu.com'
    
    ###<ATTR task_set>point to a 'TaskSet' class which defines
    #        behaviour of the user
    task_set = UserBehavior

    ###<ATTR min_wait/max_wait/wait_function>minimum and maximum
    #        wait time in milliseconds/10^-3 per simulated user,
    #        between the execution of tasks
    #
    #        By default the time is randomly chosen uniformly
    #        between min_wait and max_wait
    #
    #        any user-defined time distributions can be used by
    #        setting 'wait_function' to any arbitrary function
    #wait_function = lambda self: random.expovariate(1)*1000
    min_wait = 1
    max_wait = 1000


