#*-*coding:utf8*-*

import re
import logging
from termcolor import colored


class Logger(logging.Logger):
    """
    logging.Logger类实现,使用logging.getLogger(logger_name)获取对象.
    当构造函数name参数字符串以'.log'结尾时,写入文件.否则直接打印在console上.
    只有打印在console上的message才根据log_level区分颜色.
    """

    def __init__(self, name):
        logging.Logger.__init__(self, name, logging.DEBUG)
        self._is_file = re.match(r'.+\.log$', name)

        if self._is_file:
            self._fhandler = logging.handlers.TimedRotatingFileHandler(name, when='D', interval=1)
        else:
            self._fhandler = logging.StreamHandler()

    def set_formatter(self, formatter):
        formatter = logging.Formatter(formatter)
        self._fhandler.setFormatter(formatter)
        self.addHandler(self._fhandler)

    def debug(self, msg, *args, **kw):
        colored_msg = colored(msg, color='blue')
        self.log(logging.DEBUG, colored_msg, *args, **kw)

    def info(self, msg, *args, **kw):
        colored_msg = colored(msg, color='green')
        self.log(logging.INFO, colored_msg, *args, **kw)

    def warn(self, msg, *args, **kw):
        colored_msg = colored(msg, color='yellow')
        self.log(logging.WARNING, colored_msg, *args, **kw)

    def error(self, msg, *args, **kw):
        colored_msg = colored(msg, color='red')
        self.log(logging.ERROR, colored_msg, *args, **kw)


logging.setLoggerClass(Logger)

def get_logger(name, request=False):
    logger = logging.getLogger(name)

    if request:
        logger.set_formatter("[%(requestid)s] [%(levelname)s] [%(asctime)s] [%(process)d:%(thread)d]\n%(message)s")
    else:
        logger.set_formatter("[%(levelname)s] [%(asctime)s] [%(process)d:%(thread)d]\n%(message)s")
    return logger

