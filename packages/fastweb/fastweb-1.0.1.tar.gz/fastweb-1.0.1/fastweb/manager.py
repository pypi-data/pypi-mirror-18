# *-* coding:utf-8 *-*
from base import INFO,ERROR

from db import Mysql,Redis,Mongo
from rpc import RPC
import loader

class MysqlManager(object):

    def __init__(self):

        self._mysql_configs = {}
        self.reset()

    def reset(self):
        
        self._mysql_pools = {}
                
        mysql_components = loader.loader.config_handler.get_components('mysql')

        for name,value in mysql_components.items():
            mysql_config = loader.loader.config[name]
            self._mysql_configs[name] = mysql_config
            max_connections = int(mysql_config['max_connections'])
    
            mysql_pool = []		
        
            for i in range(max_connections):
                mysql = Mysql(**mysql_config)
                mysql_pool.append(mysql)
        
            self._mysql_pools[value['object']] = mysql_pool
    
    def __getattr__(self,name):
        if name not in self._mysql_pools.keys():
            return None

        for mysql in self._mysql_pools[name]:
            if not mysql.status:
                mysql.status = 1
                return mysql

        INFO('连接池已满')
        return Mysql(**self._mysql_configs['mysql:'+name])
        
class RedisManager(object):

    def __init__(self):
    
        self.reset()

    def reset(self):
    
        self._redis_pool = {}

        redis_components = loader.loader.config_handler.get_components('redis')

        for name,value in redis_components.items():
            redis_config = loader.loader.config[name]
            
            redis = Redis(**redis_config)
            redis.name = name
            self._redis_pool[value['object']] = redis

    def __getattr__(self,name):
        if name not in self._redis_pool.keys():
            return None

        return self._redis_pool[name]

class MongoManager(object):

    def __init__(self):
    
        self.reset()

    def reset(self):
    
        self._mongo_pool = {}

        mongo_components = loader.loader.config_handler.get_components('mongo')

        for name,value in mongo_components.items():
            mongo_config = loader.loader.config[name]
            
            mongo = Mongo(**mongo_config)
            mongo.name = name
            self._mongo_pool[value['object']] = mongo

    def __getattr__(self,name):
        if name not in self._mongo_pool.keys():
            return None

        return self._mongo_pool[name]

class RPCManager(object):

    def __init__(self):
        self._rpc_configs = {}
        self.reset()

    def reset(self):
        self._rpc_pools = {}

        rpc_components = loader.loader.config_handler.get_components('rpc')

        for name,value in rpc_components.items():
            rpc_config = loader.loader.config[name]
            self._rpc_configs[name] = rpc_config
            max_connections = int(rpc_config.get('max_connections', 10))

            rpc_pool = []

            for i in range(max_connections):
                rpc_obj = RPC(**rpc_config)
                rpc_pool.append(rpc_obj)  
         
            self._rpc_pools[value['object']] = rpc_pool

    def __getattr__(self, name):

        if name not in self._rpc_pools.keys():
            return None

        ## for rpc in self._rpc_pools[name]:
        ##     if not rpc.status:
        ##         rpc.status = 1
        ##         return rpc

        ## INFO('RPC 连接池已满') 
        return RPC(**self._rpc_configs['rpc:'+name])

