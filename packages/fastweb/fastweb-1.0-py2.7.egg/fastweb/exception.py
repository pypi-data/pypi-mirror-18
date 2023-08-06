#*-*coding:utf8*-*

class AdapterException(Exception):
    pass
        
class MysqlException(AdapterException):
    pass

class RedisException(AdapterException):
    pass
	
class MongoException(AdapterException):
    pass
	
