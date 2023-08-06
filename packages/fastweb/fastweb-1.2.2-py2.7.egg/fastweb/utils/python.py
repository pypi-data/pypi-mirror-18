# coding:utf8

"""python特性"""

import six

def to_iter(e):
    """转换可迭代形式"""
    if isinstance(e, (six.string_types, six.string_types, six.class_types, six.text_type, six.binary_type)):
        return (e)
    elif isinstance(e, list):
        return (e)
 
def to_plain(i):
    """转换不可迭代形式"""
    if isinstance(i, dict):
        plain = ''
        for key, value in i:
            plain += "{key}:{value}".format(key=key, value=value)
        return plain
    elif isinstance(i, (list, set)):
        return ','.join(i)
    else:
        return i

def mixin(cls, mixcls, resume=False):
    """动态继承"""
    mixcls = to_iter(mixcls)

    if resume:
            cls.__bases__ = mixcls
    else:
        for mcls in mixcls: 
            cls.__bases__ += (mcls,)

