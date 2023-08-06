# *-* coding:utf-8 *-*
#
#
#
#
"""
"""



from base import Base,Configer
from im import Im
from manager import (MysqlManager,RedisManager,MongoManager,RPCManager)

class Loader(object):

    def __init__(self):
        self._config = {}
        self._config_handler = None
        
        self._err_code = {}

        self._mime = {}

        self._mysql_manager = None
        self._redis_manager = None
        self._mongo_manager = None
        self._rpc_manager = None
        
        self._im = None

    def load_config(self,config_path):
        configer = Configer(config_path)
        self._config_handler = configer
        self._config = configer.config

    def load_err_code(self):
        err_code = {
                    'SUC' : {'code':0,'message':'success'},
                    'ARG' : {'code':1,'message':'invalid arguments'},
                    'SVR' : {'code':2,'message':'server error'},
                    'TOKEN' : {'code':3,'message':'invalid token'},
                    'KEY' : {'code':4,'message':'key not exist'},
                    'EXT' : {'code':5,'message':'key exist'},
                    'PWD' : {'code':6,'message':'password wrong'},
                    'FMT' : {'code':7,'message':'format error'},
                    'FT' : {'code':8,'message':'upload file type not support'},
                    9 : { 'code': 9, 'message': 'invalid resource' }
                    }

        self._err_code = err_code

    def load_mime(self):
        mime = {
                     'image/gif':'.gif',
                     'image/x-png':'.png',
                     'image/x-jpeg':'.jpeg',
                     'image/jpeg':'.jpeg',
                     'image/png':'.png'
                    }

        self._mime = mime

    def load_mysql_manager(self):
        self._mysql_manager = MysqlManager()

    def load_redis_manager(self):
        self._redis_manager = RedisManager()

    def load_mongo_manager(self):
        self._mongo_manager = MongoManager()

    def load_im(self):
        org_name = self._config['server:im']['org_name']
        app_name = self._config['server:im']['app_name']
        client_id = self._config['server:im']['client_id']
        client_secret = self._config['server:im']['client_secret']
        self._im = Im(org_name,app_name,client_id,client_secret)

    def load_rpc_manager(self):
        self._rpc_manager = RPCManager()

    @property
    def config(self):
        return self._config

    @property
    def config_handler(self):
        return self._config_handler

    @property
    def err_code(self):
        return self._err_code

    @property
    def mime(self):
        return self._mime

    @property
    def mysql_manager(self):
        return self._mysql_manager

    @property
    def redis_manager(self):
        return self._redis_manager

    @property
    def mongo_manager(self):
        return self._mongo_manager

    @property
    def im(self):
        return self._im

    @property
    def rpc_manager(self):
        return self._rpc_manager

loader = Loader()


