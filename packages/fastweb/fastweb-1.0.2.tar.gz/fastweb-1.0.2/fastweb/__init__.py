# *-*coding:utf8*-*

from tornado.gen import coroutine
from tornado.web import UIModule as UI
from tornado.options import options
from tornado import (web,httpserver,ioloop)

from base import INFO


def start_server(port, handlers, **settings):
    """启动服务器"""

    application = web.Application(
        handlers,
        **settings
    )   

    http_server = httpserver.HTTPServer(application,xheaders = settings.get('xheaders'))
    http_server.listen(port)
    INFO('Server Start on {port}'.format(port=port))
    ioloop.IOLoop.instance().start()
    INFO('Server Stop on {port}'.format(port=port))

    
