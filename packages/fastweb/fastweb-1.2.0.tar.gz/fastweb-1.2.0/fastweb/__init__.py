# *-*coding:utf8*-*


from tornado.options import options
from tornado.gen import (coroutine, Return, Task)
from tornado import (gen, web, httpserver, ioloop)
from tornado.web import (UIModule as UI, asynchronous)
from tornado.httpclient import HTTPRequest as Request

from fastweb.loader import gl
from fastweb.utils.log import get_logger
from fastweb.core import (Api, Page, Component, AsynComponent, catchError, checkArgument)

logger = get_logger('fastweb')


def start_server(port, handlers, **settings):
    """启动服务器"""

    application = web.Application(
        handlers,
        **settings
    )

    http_server = httpserver.HTTPServer(
        application, xheaders=settings.get('xheaders'))
    http_server.listen(port)
    logger.info('Server Start on {port}'.format(port=port))
    ioloop.IOLoop.instance().start()
    logger.info('Server Stop on {port}'.format(port=port))


def set_errcode_handler(**kwargs):
    pass
