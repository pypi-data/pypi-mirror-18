# coding:utf8

import redis
import tornadis
from copy import deepcopy
from tornado.locks import Condition
from redis.exceptions import RedisError
from tornadis.exceptions import ConnectionError

from fastweb import ioloop
import fastweb.utils.tool as tool
from fastweb import coroutine, Return
from fastweb.exception import RedisError
from fastweb.utils.log import get_logger
from fastweb.component import BaseComponent

logger = get_logger(__name__)

DEFAULT_PORT = 6379
DEFAULT_TIMEOUT = 5


class Redis(BaseComponent):
        
    def __init__(self,**kwargs):
        super(Redis, self).__init__()
        self.reset(**kwargs)
        
    def reset(self,**kwargs):
        self.set_idle()
        self._redis = None

        redis_config = {'host':kwargs['host'],'port':int(kwargs['port']),'password':kwargs.get('password'),
                        'db':int(kwargs.get('db')),'socket_timeout':int(kwargs.get('timeout')),'charset':kwargs.get('charset')}

        self._redis = redis.StrictRedis(**redis_config)


    def persist(self,name):
        try:
            ret = self._redis.persist(name)       
            self._logger('INFO', 'Redis persist  -- redis command[persist %s]' % (name))
        except RedisError:
            raise RedisError
        return ret

    def srem(self,name,*values):
        try:
            ret = self._redis.srem(name,*values)       
            self._logger('INFO', 'Redis srem  -- redis command[srem %s %s]' % (name,values))
        except RedisError:
            raise RedisError
        return ret

    def sismember(self,name,value):
        try:
            ret = self._redis.sismember(name,value)       
            self._logger('INFO', 'Redis sismember -- redis command[sismember %s %s]' % (name,value))
        except RedisError:
            raise RedisError
        return ret

    def incr(self,name,amount = 1):
        try:
            ret = self._redis.incr(name,amount)       
            self._logger('INFO', 'Redis incr -- redis command[incr %s %d]' % (name,amount))
        except RedisError:
            raise RedisError
        return ret

    def get(self,name):
        try:
            ret = self._redis.get(name)       
            self._logger('INFO', 'Redis get -- redis command[get %s]' % name)
        except RedisError:
            raise RedisError
        return ret

    def setnx(self,name,value):
        try:
            ret = self._redis.setnx(name,value)       
            self._logger('INFO', 'Redis setnx -- redis command[setnx %s %s]' % (name,value))
        except RedisError:
            raise RedisError
        return ret

    def hmset(self,name,arg_dict):
        try:
            ret = self._redis.hmset(name,arg_dict)       
            self._logger('INFO', 'Redis hmset -- redis command[hmset %s %s]' % (name,arg_dict))
        except RedisError:
            raise RedisError
        return ret

    def hset(self,name,key,value):
        try:
            ret = self._redis.hset(name,key,value)       
            self._logger('INFO', 'Redis hset -- redis command[hset %s %s %s]' % (name,key,value))
        except RedisError:
            raise RedisError
        return ret

    def hget(self,name,key):
        try:
            ret = self._redis.hget(name,key)
            self._logger('INFO', 'Redis hget -- redis command[hget %s %s]' % (name,key))
        except RedisError:
            raise RedisError
        return ret

    def hmget(self,name,*args):
        try:
            ret = self._redis.hmget(name,*args)  
            self._logger('INFO', 'Redis hmget -- redis command[hmget %s %s]' % (name,args))
        except RedisError:
            raise RedisError
        return ret

     
    def hgetall(self,name):
        try:
            ret =  self._redis.hgetall(name)       
            self._logger('INFO', 'Redis hgetall -- redis command[hgetall %s]' % name)
        except RedisError:
            raise RedisError
        return ret

    def exists(self,name):
        try:
            ret = self._redis.exists(name)       
            self._logger('INFO', 'Redis exists -- redis command[exists %s]' % (name))
        except RedisError,e:
            raise RedisError
        return ret 

    def setex(self,name,time,value):
        try:
            ret = self._redis.setex(name,time,value)
            self._logger('INFO', 'Redis setex -- redis command[setex %s %d %s]' % (name,time,value))
        except RedisError:
            raise RedisErrors

        return ret

    def set(self,name,value):
        try:
            ret = self._redis.set(name,value)
            self._logger('INFO', 'Redis set -- redis command[set %s %s]' % (name,value))
        except RedisError:
            raise RedisErrors
        return ret

    def expire(self,name,time):
        try:
            ret = self._redis.expire(name,time)
            self._logger('INFO', 'Redis expire -- redis command[expire %s %d]' % (name,time))

        except RedisError:
            raise RedisErrors
        return  ret

    def delete(self,*name):
        try:
            ret = self._redis.delete(*name)
            self._logger('INFO', 'Redis delete -- redis command[delete %s]' % name)
        except RedisError:
            raise RedisError
        return ret


class AsynRedis(BaseComponent):
    """异步redis组件"""

    def __init__(self, **kwargs):
        self.rebuild(kwargs)

    @coroutine
    def rebuild(self, kwargs):
        super(AsynRedis, self).__init__()

        self._redis = None

        self.host = kwargs.get('host')
        assert self.host, '`host` is essential of redis'
        self.port = kwargs.get('port', DEFAULT_PORT)
        self.password = kwargs.get('password', None)
        self.timeout = kwargs.get('timeout', DEFAULT_TIMEOUT)
        self.db = kwargs.get('db', 0)

        self.redis_config = {'host': self.host,
                             'port': int(self.port),
                             'password': self.password,
                             'connect_timeout': int(self.timeout),
                             'autoconnect': True, 
                             'db': int(self.db)}

        self._connect_condition = Condition()

        try:
            self.set_idle()
            self._redis = tornadis.Client(**self.redis_config)
            yield self._redis.connect()
            self._connect_condition.notify()
        except ConnectionError as ex:
            self.set_error(ex)


    def __str__(self):
        return '<AsynRedis {host} {port} {name}>'.format(
            host=self.host, port=self.port, name=self.name)

    @coroutine
    def call(self, *args, **kwargs):
        """执行redis命令"""

        if not self._redis.is_connected:
            yield self._connect_condition.wait()

        if self._redis.is_connected:
            with tool.timing('s', 10) as t:
                future = yield self._redis.call(*args, **kwargs) 
            self._logger('INFO', 'Redis Command [{command}] -- [{time}]'.format(command=' '.join(str(v) for v in args), time=t))
            raise Return(future)

