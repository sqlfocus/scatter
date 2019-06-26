#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os
import sys
import time

import tornado.ioloop
import tornado.options
import tornado.web

###options
#  python3 xxx.py --port=9000
#  python3 xxx.py --help
tornado.options.define("port", default=80, help="server port", type=int)
tornado.options.define("period", default=3, help="period of self-timer, s", type=int)


class BaseHandler(tornado.web.RequestHandler):
    '''
    base for all handler class
    '''
    def write_error(self, status_code, **kwargs):
        '''
        self defined error return
        '''
        #after error occur, capture it and customize log
        if kwargs.get("sdm", None) is not None:
            logging.getLogger().exception("{}: {}, {}, body[{}]".format(
                self._reason, self.request.method, self.request.uri,
                self.request.body), exc_info=True)
            
        #customize error msg
        resp = {"ret":-1,"msg":kwargs.get("sdm", "error")}
        self.write(resp)

class PingHandler(BaseHandler):
    '''
    handler class to dispose URL
    '''
    def get(self):
        self.write("pong")
    def post(self):
        ###hit BaseHandler.write_error()
        ###curl -X POST -d '{"test":"string"}' http://localhost/
        self.send_error(405, sdm="not support post")
        return

        ###do something others
        pass

    def delete(self):
        ###curl -X DELETE http://localhost/
        self.send_error(405, sdm="not support delete")
        return


def period_loop(app):
    '''
    param app [obj] tornodo application
    return None
    '''
    print("hi, {}".format(time.time()))
    
class Application(tornado.web.Application):
    def __init__(self):
        ###URL router
        handlers = [
            (r"/", tornado.web.RedirectHandler, dict(url=r"/ping")),
            (r"/ping", PingHandler),
        ]
        
        ###global setting
        settings = {
            #path for tornado template
            "template_path":os.path.join(os.path.dirname(__file__), "templates"),
            #debug feature: = autoreload=True
            #                 + compiled_template_cache=False
            #                 + static_hash_cache=False
            #                 + serve_traceback=True
            "debug":True
        }
        tornado.web.Application.__init__(self, handlers, **settings)

        ###period timer
        self.timer = tornado.ioloop.PeriodicCallback(
            lambda: period_loop(self),
            tornado.options.options.period * 1000,
            0)
        
def main():
    ###pase config file and command line
    #tornado.options.parse_config_file(
    #    os.path.join(os.path.dirname(__file__), "conf/varyag.conf"),
    #    final=False
    #)
    tornado.options.parse_command_line()
    
    ###create http server
    app = Application()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(tornado.options.options.port)

    ###start
    app.timer.start()
    tornado.ioloop.IOLoop.current().start()

    ###exit
    sys.exit("You really need exit???!!!")

if __name__ == "__main__":
    sys.exit(main())
