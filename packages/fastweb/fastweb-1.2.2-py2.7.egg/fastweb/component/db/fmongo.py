#coding:utf8

from pymongo import MongoClient
from motor import motor_tornado
from tornado.locks import Condition
from tornado.gen import coroutine, Return
from pymongo.errors import ConnectionFailure,PyMongoError

import fastweb.utils.tool as tool
from fastweb import ioloop
from fastweb.utils.log import get_logger
from fastweb.exception import MongoError
from fastweb.component import BaseComponent

logger = get_logger(__name__)

DEFAULT_PORT = 27017
DEFAULT_TIMEOUT = 5


class Mongo(BaseComponent):
    
    def __init__(self,**args):
        self.reset(**args)

    def reset(self,**args):
        self._mongo = None
        self._db = None
        self._collection = None
        
        mongo_config = {'host':args['host'],'port':int(args['port']),'connectTimeoutMS':int(args['timeout'])}

        try:
            self._mongo = MongoClient(**mongo_config)
        except ConnectionFailure,e:
            EROR('Mongo Error -- connect failed[%s]' % e)
            raise MongoError

    def find(self,filter=None,projection=None,skip=0,limit=0,no_cursor_timeout=False,sort=None,allow_partial_results=False,\
             oplog_replay=False, modifiers=None, manipulate=True):
        return self._collection.find(filter=filter,projection=projection,skip=skip,limit=limit,no_cursor_timeout=no_cursor_timeout,\
               modifiers=modifiers, manipulate=manipulate)
    
    def count(self):
        return self._collection.count()

    def select(self,db,collection):
        self._db = self._mongo[db]
        self._collection = self._db[collection]

    def select_db(self,db):
        self._db = self._mongo[db]

    def select_collection(self,collection):
        self._collection = self._db[collection]

    def insert_one(self,data):
        try:
            obj_id = str(self._collection.insert_one(data).inserted_id)
            INFO('Mongo insert -- data[%s] -- ret[%s]' % (data,obj_id))
            return obj_id
        except PyMongoError:    
            raise MongoError

    def collection_names(self,system = True):
        return self._db.collection_names(include_system_collections = system)


class AsynMongo(BaseComponent):
    """异步Mongo组件"""

    def __init__(self, **kwargs):
        super(AsynMongo, self).__init__()
        self.rebuild(kwargs)

    def __str__(self):
        return '<AsynMongo {host} {port} {name}>'.format(
            host=self.host, port=self.port, name=self.name)

    @coroutine
    def rebuild(self, kwargs):
        """重建组件"""

        self._client = None
        self._db = None
        self._collection = None

        self.host = kwargs.get('host')
        assert self.host, '`host` is essential of mongo'
        self.port = kwargs.get('port', DEFAULT_PORT)
        self.timeout = kwargs.get('timeout', DEFAULT_TIMEOUT)

        mongo_config = {
            'host': self.host, 'port': int(self.port), 'connectTimeoutMS': int(self.timeout)}

        self._connect_condition = Condition()

        try:
            self.set_idle()
            self._client = motor_tornado.MotorClient(**mongo_config)
            yield self._client.open()
            self._connect_condition.notify()
        except ConnectionFailure as ex:
            self.set_error(ex)

    def select(self, db, collection):
        """选择db和collection"""

        self._db = self._client[db]
        self._collection = self._db[collection]
        self._logger(
            'INFO',
            'Mongo Command [use {db}]\t[{db}.{cl}]'.format(
                db=db,
                cl=collection))

    def select_db(self, db):
        """选择db"""

        self._db = self._client[db]
        self._logger('INFO', 'Mongo Command [use {db}]'.format(db=db))

    def select_collection(self, collection):
        """选择collection"""

        self._collection = self._db[collection]
        self._logger('INFO', 'Mongo Command [{db}.{cl}]'.format(db=self._db.name, cl=collection))

    @coroutine
    def find_one(self, spec_or_id=None, callback=None, *args, **kwargs):
        """查找一个document"""

        if not self._client.alive():
            yield self._connect_condition.wait()

        if self._client.alive() and self._collection:
            with tool.timing('s', 10) as t:
                future = yield self._collection.find_one(spec_or_id=spec_or_id, callback=callback, *args, **kwargs)
            self._logger('INFO', 'Mongo Command [{db}.{cl}.find({query})] -- [{time}]'.format(db=self._db.name, cl=self._collection.name, query=spec_or_id, time=t))
            raise Return(future)

    @coroutine
    def find(self, *args, **kwargs):
        """查找document"""

        if not self._client.alive():
            yield self._connect_condition.wait()

        if self._client.alive() and self._collection:
            with tool.timing('s', 10) as t:
                future =  yield self._collection.find(*args, **kwargs)
            self._logger('INFO', 'Mongo Command [{db}.{cl}.find({query}).limit({limit})] -- [{time}]'.format(db=self._db.name, cl=self._collection.name, query=kwargs.get('query'), limit=kwargs.get('limit'), time=t))
            raise Return(future)

    @coroutine
    def find_and_modify(self, query={}, update=None, upsert=False, sort=None, full_response=False, manipulate=False, callback=None, **kwargs):
        """查找并修改document"""

        if not self._client.alive():
            yield self._connect_condition.wait()

        if self._client.alive() and self._collection:
            with tool.timing('s', 10) as t:
                future = yield self._collection.find_and_modify(query={}, update=update, upsert=upsert, sort=sort, full_response=full_response, manipulate=manipulate, callback=callback, **kwargs)
            self._logger('INFO', 'Mongo Command [find and modify] -- [dur]'.format(time=t))
            raise Return(future)
    
    @coroutine
    def insert(self, doc_or_docs, manipulate=True, safe=None, check_keys=True, continue_on_error=False, callback=None, **kwargs):
        """插入document"""

        if not self._client.alive():
            yield self._connect_condition.wait()

        if self._client.alive() and self._collection:
            with tool.timing('s', 10) as t:
                future = self._collection.insert(doc_or_docs, manipulate=manipulate, safe=safe, check_keys=check_keys, continue_on_error=continue_on_error, callback=callback, **kwargs)
            self._logger('INFO', 'MOngo Command [insert] -- [time]'.format(time=t))
            raise Return(future)

    def close(self):
        self._client.disconnect()

    def __del__(self):
        self.close()
