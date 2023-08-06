# coding:utf8

import sys
import traceback
from tornado.ioloop import IOLoop

#from fastweb.core import (Api, Page)
from celery import (Celery, platforms)
from fastweb.utils.python import to_plain
from fastweb.utils.track import get_simple_meta_data
        

def get_celery_from_object(name, obj=None):
    """获取celery对象"""

    platforms.C_FORCE_ROOT = True
    celery = Celery(name)
    obj and celery.config_from_object(obj)
    return celery


class timing(object):
    """计时器"""
    __unitfactor = {'s': 1,
                    'ms': 1000,
                    'us': 1000000}

    def __init__(self, unit='s', precision=4):
        self.start = None
        self.end = None
        self.total = 0
        self.unit = unit
        self.precision = precision

    def __enter__(self):
        if self.unit not in timing.__unitfactor:
            raise KeyError('Unsupported time unit.')
        self.start = IOLoop.current().time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = IOLoop.current().time()
        self.total = (self.end - self.start) * timing.__unitfactor[self.unit]
        self.total = round(self.total, self.precision)

    def __str__(self):
        return '{total}{unit}'.format(total=self.total, unit=self.unit)


