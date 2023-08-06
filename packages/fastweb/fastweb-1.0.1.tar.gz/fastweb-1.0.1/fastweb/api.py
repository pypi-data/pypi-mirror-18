# *-*coding:utf8*-*
#
# Copyright 2015 Adapter
#
import json
import urllib
from tornado import web
from tornado.gen import coroutine,Return
from tornado.httpclient import AsyncHTTPClient,HTTPRequest as Request

from base import Base
from base import ERROR,INFO
from loader import loader

class Component(object):

    def __init__(self):
        self._mysqls = {}
        self._rpcs = {}

    def __getattr__(self,name):
        if name in self._mysqls.keys():
            return self._mysqls[name]

#        if name in self._rpcs.keys():
#            return self._rpcs[name]

        if loader.mysql_manager:
            mysql = getattr(loader.mysql_manager,name)

            if mysql:
                self._mysqls[name] = mysql
                return mysql

        if loader.rpc_manager:
            rpc = getattr(loader. rpc_manager, name)

            if rpc:
                self._rpcs[name] = rpc
                return rpc

        if loader.redis_manager:
            redis = getattr(loader.redis_manager,name)

            if redis:
                return redis

        if loader.mongo_manager:    
            mongo = getattr(loader.mongo_manager,name)

            if mongo:
                return mongo

        if name in ('_new_cookie'):
            raise AttributeError

        ERROR('CONF ERR -- component_name[%s]' % name)
        raise AttributeError

    @property
    def config(self):
        return loader.config

    @property
    def http_client(self):
        return AsyncHTTPClient()

    def __del__(self):
        for name,mysql in self._mysqls.items():
            mysql.status = 0
            del self._mysqls[name]

        for name,rpc in self._rpcs.items():
            rpc.status = 0
            del self._rpcs[name]


class API(web.RequestHandler,Component):
    """API baseclass.
    
    Api need inherit this class.

    Example:

        from api import API
        
        class CreateUser(API):
            def post(self._:
                pass
            def get(self._:
                pass
            ...
    """

    def __init__(self, application, request, **kwargs):
        super(API,self).__init__(application, request, **kwargs)

        self._ret = {}
        self._uri = request.uri
        self._remote_ip = request.remote_ip
        self._host = request.host

        INFO('API IN -- remote_ip[%s] -- api[%s%s] -- arg[%s] -- User-Agent[%s]' 
                      % (self._remote_ip,self._host,self._uri,self.request.arguments, self.request.headers['User-Agent']))	

    @property
    def loader(self):
        return loader

    @property
    def err_code(self):
        return loader.err_code

    @property
    def mime(self):
        return loader.mime

    @property
    def im(self):
        return loader.im

    @property
    def arguments(self):
        arguments = {}

        for key,value in self.request.arguments.items():
            value = ''.join(value)
            arguments[key] = value

        return arguments

    @property
    def host(self):
        return self._host

    @property
    def remote_ip(self):
        return self._remote_ip

    def check_arguments(self,*keys):
        enssential_keys = set(keys)

        arguments = set(self.request.arguments.keys())

        if Base.check_arguments(arguments,enssential_keys):
            diff_key =  enssential_keys.symmetric_difference(arguments)

            ERROR('ARG ERR -- diff arg[%s]' % diff_key)

            return True

    def check_arguments_empty(self,*keys):
        if 0 == len(keys):
            keys = self.request.arguments.keys()

        for key in keys:
            if key not in self.request.arguments.keys() or Base.empty(''.join(self.request.arguments[key])):
                ERROR('ARG ERR -- empty arg[%s]' % key)

                return True

    def set_ajax_cors(self,allow_ip):
        self.set_header('Access-Control-Allow-Origin',allow_ip)	

        INFO('SET HEADER -- set cors[%s]' % allow_ip)	

    def set_header_json(self):
        self.add_header('Content-type','text/json')

    def end(self,code = 'SUC', **add_dict):
        self._ret = loader.err_code[code]
        self._ret = dict(self._ret,**add_dict)
        self.write(json.dumps(self._ret))
        self.finish()
        INFO('API OUT -- remote_ip[%s] -- api[%s%s] -- ret[%s]' 
            % (self._remote_ip, self._host, self._uri, self._ret))	





