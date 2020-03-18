#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
install: pip3 install sanic
doc refer: https://sanic.readthedocs.io/en/latest/index.html
'''
import sanic


async def index(request):
    '''
    限定访问方法
    curl http://127.0.0.1:9000/
    curl http://127.0.0.1:9000/?arg1=1&arg2=test
    '''
    return sanic.response.json(
        {
            "request.url":request.url,
            "request.args":request.args,
            "request.body":request.body,  #body
            "request.json":request.json,  #body by json format
        }
    )

async def number_handler(request, arg):
    '''
    通过'<>'，指定参数，并限定参数类型
    curl http://127.0.0.1:9000/number/1
    '''
    #return sanic.response.raw("raw data")
    #return sanic.response.text("hello world")
    #return sanic.response.html("<p>hello world</p>")
    #return await sanic.response.file("/path/to/some/file")
    #return sanic.response.redirect("/index")
    return sanic.response.json(
        {"number":arg},
        headers = {'X-Served-By':'sanic'},
        status = 200
    )



if __name__ == "__main__":
    app = sanic.Sanic(__name__)
    
    ###添加路由
    #format 1: 限定访问方法
    app.add_route(index, "/", methods=["GET","POST"])
    #format 2: 限定URL式参数及类型
    app.add_route(number_handler, "/number/<arg:int>")
    #format 3: 静态文件
    app.static("/README", "./README.md")

    ###开启监听
    app.run(host="0.0.0.0", port=9000,
            workers=1,
            debug=True,        #支持在线调整代码
            access_log=True    #INFO日志，关闭以提升性能
    )
