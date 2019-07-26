#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os
import sys
import time

import tornado.options
import tornado.web

###send ourself
_FNAME = "tornado_http_bigfile.py"
_FPATH = os.path.join(os.getcwd(), _FNAME)

class BigfileHandler(tornado.web.RequestHandler):
    async def get(self):
        self.set_header('Content-Type','application/octet-stream')
        self.set_header('Content-Disposition', 'attachment; filename=' + _FNAME)
        buf_size = 4096
        with open(_FPATH, 'rb') as f:
            while True:
                data = f.read(buf_size)
                if not data:
                    break
                self.write(data)
                await self.flush()
        self.finish()


class Application(tornado.web.Application):
    def __init__(self):
        ###URL router
        handlers = [
            (r"/bigfile", BigfileHandler),
        ]
        
        ###global setting
        settings = {
            #debug feature: = autoreload=True
            #                 + compiled_template_cache=False
            #                 + static_hash_cache=False
            #                 + serve_traceback=True
            "debug":True
        }
        tornado.web.Application.__init__(self, handlers, **settings)

        
def main():
    app = Application()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(80)
    tornado.ioloop.IOLoop.current().start()
    sys.exit("You really need exit???!!!")

if __name__ == "__main__":
    '''
    test using 
       curl http://localhost/bigfile
    or
       import urllib.request
       req = urllib.request.urlopen("http://localhost/bigfile")
       req.read()
    '''
    sys.exit(main())
