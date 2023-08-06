# coding:utf8

from fastweb import ioloop
from fastweb.utils.log import get_logger

#空闲状态
IDLE = 0
#使用状态
USED = 1
#错误状态
ERROR = 2

logger = get_logger(__name__)


class BaseComponent(object):
    """组件基类"""

    def __init__(self):
        self.name = ''
        self._logger = None
        self.status = None
        self.message = None

    def set_used(self, logfunc):
        self.set_logger(logfunc)
        self.status = USED

    def set_idle(self):
        self.status = IDLE

    def set_error(self, message):
        self.status = ERROR
        self.message = message
    
    def set_logger(self, logfunc):
        self._logger = logfunc
