# coding:utf8

"""异常类"""


class FastWebException(Exception):
    pass

class MysqlError(FastWebException):
    pass

class RedisError(FastWebException):
    pass

class MongoError(FastWebException):
    pass

class RpcError(FastWebException):
    pass

class ConfigError(FastWebException):
    pass


