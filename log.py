#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#pip3.x install ConcurrentLogHandler
from cloghandler import ConcurrentRotatingFileHandler
import logging
import logging.handlers
import os
import sys

'''
tornado提供的日志模块儿tornado.log也是封装的python原生态日志
模块logging；因此1）为了解原生态接口及使用方法，2）降低耦合
度，进一步支持函数式编程，本项目采用原生态python模块

<NOTE>
  1) 可以利用 logger.error("msg", exc_info=True) 打印错误执行信息
  2) 可以利用 logger.exception("msg", Exception) 打印错误执行信息
  3) 日志中消息组织形式("hello %s", "world")优于("hello {}".format("world"))
'''

###创建日志目录
__LOG_DIR = "/opt/logs"
if not os.path.isdir(__LOG_DIR):
    os.makedirs(__LOG_DIR, mode=0o777)

###初始化日志实例，依赖于模块初始化只调用一次的特性
log = logging.getLogger("project-name")
log.setLevel(level=logging.DEBUG)   #级别必须<=后续handler级别

# 打印调试输出到终端界面
__stream_handler = logging.StreamHandler(sys.stdout)
__stream_handler.setFormatter(
    logging.Formatter(
        "%(filename)s[line:%(lineno)d] - %(message)s"
    )
)
__stream_handler.setLevel(level=logging.DEBUG)
log.addHandler(__stream_handler)

# 打印到日志文件，<TK!!!>log目录必须提前创建好
#__file_handler = logging.handlers.RotatingFileHandler(
__file_handler = logging.handlers.ConcurrentRotatingFileHandler(  #支持多进程
    filename=os.path.join(__LOG_DIR, "mdms.log"),
    maxBytes=10000000, backupCount=3
)
__file_handler.setFormatter(
    logging.Formatter(
        "%(asctime)s - %(name)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s"
    )
)
__file_handler.setLevel(level=logging.DEBUG)
log.addHandler(__file_handler)



##################use by other module###################
#from log import log
#log.debug("hello, {}".format("world"))
#log.info("hello, {}".format("world"))
#log.warn("hello, {}".format("world"))
#log.error("hello, {}".format("world"))
########################################################




