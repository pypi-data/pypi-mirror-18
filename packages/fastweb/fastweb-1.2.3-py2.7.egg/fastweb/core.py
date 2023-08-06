# coding:utf8

import json
import types
import shlex
import traceback
import subprocess
#from threading import Lock
from multiprocessing import Lock

from tornado import (ioloop, web)
from tornado.locks import Condition
from tornado.process import Subprocess
from tornado.gen import (coroutine, Task, Return)
from tornado.httpclient import (HTTPClient, AsyncHTTPClient, HTTPRequest as Request)

from fastweb.loader import gl
from fastweb.utils.tool import timing
from fastweb.utils.base import uniqueid
from fastweb.utils.python import to_plain


class Component(object):
    """组件基类,组件操作"""

    _black_list = ['requestid', '_new_cookie', 'include_host', '_active_modules', '_current_user', '_locale']

    def __init__(self):
        self._components = {}
        self.gen_requestid()
        gl.manager.set_logger(self.recorder)
        self.http_client = HTTPClient()
        self._component_lock = Lock()

    def __getattr__(self, name):
        """获取组件"""

        if name in self._black_list:
            raise AttributeError

        obj = self._components.get(name)

        if not obj:
            self._component_lock.acquire()
            obj = getattr(gl.manager, name)
            self._component_lock.release()

            if not obj:
                self.recorder('ERROR', "can't acquire idle component [{name}]".format(name=name))
                raise AttributeError

            self._components[name] = obj
            return obj
        else:
            return obj          

    @property
    def config(self):
        """配置文件"""

        return gl.config

    def gen_requestid(self):
        self.requestid = uniqueid()

    def call_subprocess(self, command, stdin_data=None):
        """调用命令行"""

        with timing('s', 10) as t:
            sub_process = subprocess.Popen(shlex.split(command),
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            
            result, error = sub_process.communicate(stdin_data)

        self.recorder('INFO', 'Call Subprocess Command [{command}] -- result[{result}] -- [{time}]'.format(command=command, time=t, result=result.strip() if result else error.strip() ))
        return (result, error)

    def add_function(self, **kwargs):
        """增加方法到对象中"""
        
        for callname,func in kwargs.iteritems():
            setattr(self, '{callname}'.format(callname=callname), types.MethodType(func, self))

    def recorder(self, level, message):
        """日志记录"""

        level = level.lower()
        level_dict = {
            'info': gl.request_logger.info,
            'debug': gl.request_logger.debug,
            'warn': gl.request_logger.warn,
            'error': gl.request_logger.error}
        level_dict[level](message, extra={'requestid': self.requestid})

    def release(self):
        for component in self._components.values():
            component.set_idle()
        self.recorder('DEBUG', 'Idle All Used Component')


class AsynComponent(object):
    """异步组件基类,异步组件操作"""

    _black_list = ['requestid', '_new_cookie', 'include_host', '_active_modules', '_current_user', '_locale']

    def __init__(self):
        self._components = {}
        self.gen_requestid()
        gl.manager.set_logger(self.recorder)

    def __getattr__(self, name):
        """获取组件"""

        if name in self._black_list:
            raise AttributeError

        obj = self._components.get(name)
        
        if not obj:
            obj = getattr(gl.manager, name)

            if not obj:
                self.recorder('ERROR', "can't acquire idle component [{name}]".format(name=name))
                raise AttributeError

            obj.set_used(self.recorder)
            self._components[name] = obj
            return obj
        else:
            return obj          

    def gen_requestid(self):
        self.requestid = uniqueid()

    @property
    def config(self):
        """配置文件"""

        return gl.config

    @property
    def http_client(self):
        """异步http客户端"""

        return AsyncHTTPClient()

    @coroutine
    def call_subprocess(self, command, stdin_data=None, stdin_async=True):
        """异步调用命令行"""

        with timing('s', 10) as t:
            stdin = Subprocess.STREAM if stdin_async else subprocess.PIPE
            sub_process = Subprocess(shlex.split(command),
                                 stdin=stdin,
                                 stdout=Subprocess.STREAM,
                                 stderr=Subprocess.STREAM)
            
            if stdin_data:
                if stdin_async:
                    yield Task(sub_process.stdin.write, stdin_data)
                else:
                    sub_process.stdin.write(stdin_data)

            if stdin_async or stdin_data:
                sub_process.stdin.close()

            result, error = yield [Task(sub_process.stdout.read_until_close),
                                   Task(sub_process.stderr.read_until_close)]

        self.recorder('INFO', 'Call Subprocess Command [{command}] -- result[{result}] -- [{time}]'.format(command=command, time=t, result=result.strip() if result else error.strip() ))
        raise Return((result, error))

    def add_function(self, **kwargs):
        """增加方法到对象中"""
        
        for callname,func in kwargs.iteritems():
            setattr(self, '{callname}'.format(callname=callname), types.MethodType(func, self))

    def recorder(self, level, message):
        """日志记录"""

        level = level.lower()
        level_dict = {
            'info': gl.request_logger.info,
            'debug': gl.request_logger.debug,
            'warn': gl.request_logger.warn,
            'error': gl.request_logger.error}
        level_dict[level](message, extra={'requestid': self.requestid})

    def release(self):
        for component in self._components.values():
            component.set_idle()
        self.recorder('DEBUG', 'Idle All Used Component')


class Api(web.RequestHandler, AsynComponent):
    """API基类,API操作"""

    def __init__(self, application, request, **kwargs):
        super(Api, self).__init__(application, request, **kwargs)

        self._ret = {}
        self._uri = request.uri
        self._remote_ip = request.remote_ip
        self._host = request.host
        self.arguments = self.request.arguments
        self.requestid = ''.join(self.request.arguments.get('requestid') ) if self.request.arguments.get('requestid') else self.requestid

        self.recorder(
            'INFO',
            'API IN -- remote_ip[{ip}] -- api[{host}{uri}] -- arg[{arguments}] -- User-Agent[{agent}]'.format(
             ip=self._remote_ip,
             host=self._host,
             uri=self._uri,
             arguments=self.arguments,
             agent=self.request.headers['User-Agent']))

    @property
    def loader(self):
        """获取全局变量"""

        return gl

    @property
    def err_code(self):
        """获取错误码"""

        return gl.err_code

    @property
    def mime(self):
        """获取mime码"""

        return gl.mime

    @property
    def host(self):
        """获取host"""

        return self._host

    @property
    def remote_ip(self):
        """获取访问IP"""

        return self._remote_ip

    def log_exception(self, typ, value, tb):
        """日志记录异常"""

        self.end('SVR')
        self.recorder('ERROR', '{message}'.format(message=traceback.format_exc()))

    def set_ajax_cors(self, allow_ip):
        """设置cors"""

        self.set_header('Access-Control-Allow-Origin', allow_ip)
        self.recorder('INFO', 'SET HEADER -- set cors[{}]'.format(allow_ip))

    def set_header_json(self):
        """设置返回格式为json"""

        self.add_header('Content-type', 'text/json')
        self.recorder('INFO', 'SET HEADER -- Set Response Json')
    
    def end(self, code='SUC', log=True, **kwargs):
        """ 请求结束"""

        self._ret = gl.err_code[code]
        self._ret = dict(self._ret, **kwargs)
        self.write(json.dumps(self._ret))
        self.finish()
        #释放掉组件的使用权
        self.release()
        if log:
            self.recorder(
                'INFO', 
                'API OUT -- remote_ip[{ip}] -- api[{host}{uri}] -- ret[{ret}]'.format(
                    ip=self._remote_ip, host=self._host, uri=self._uri, ret=self._ret))
        else:
            self.recorder(
                'INFO', 
                'API OUT -- remote_ip[{ip}] -- api[{host}{uri}]'.format(
                    ip=self._remote_ip, host=self._host, uri=self._uri))



class Page(web.RequestHandler, AsynComponent):
    """Page基类,Page操作"""

    def __init__(self, application, request, **kwargs):
        super(Page, self).__init__(application, request, **kwargs)

        self._ret = {}
        self._uri = request.uri
        self._remote_ip = request.remote_ip
        self._host = request.host
        self.arguments = self.request.arguments
        self.requestid = ''.join(self.request.arguments.get('requestid') ) if self.request.arguments.get('requestid') else self.requestid

        self.recorder(
            'INFO',
            'Page IN -- remote_ip[%s] -- api[%s%s] -- arg[%s] -- User-Agent[%s]' %
            (self._remote_ip,
             self._host,
             self._uri,
             self.request.arguments,
             self.request.headers['User-Agent']))

    @property
    def loader(self):
        """获取全局变量"""

        return gl

    @property
    def mime(self):
        """获取mime码"""

        return gl.mime

    def log_exception(self, typ, value, tb):
        """日志记录异常"""

        self.recorder('ERROR', '{message}'.format(message=traceback.format_exc()))

    def end(self, template=None, log=True, **kwargs):
        """ 请求结束"""

        if template:
            self.render(template, **kwargs)

        #释放掉组件使用权
        self.release()
        if log:
            self.recorder(
                'INFO', 'Page OUT -- remote_ip[{ip}] -- api[{host}{uri}] -- template[{template}] -- variable[{variable}]'.format(
                    ip=self._remote_ip, host=self._host, uri=self._uri, template=template, variable=kwargs))
        else:
            self.recorder(
                'INFO', 
                'API OUT -- remote_ip[{ip}] -- api[{host}{uri}] -- template[{template}]'.format(
                    ip=self._remote_ip, host=self._host, uri=self._uri, template=template))


def checkArgument(convert=None, **ckargs):
    """检查请求参数"""

    def _deco(fn):
        def _wrap(cls, *args, **kwargs):
            if convert:
                for cname, ctype in convert.iteritems():
                    cvalue = cls.request.arguments.get(cname)
                    cvalue = to_plain(cvalue)
                    if cvalue:
                        cls.request.arguments[cname] = ctype(cvalue)
        
            for cname, ctype in ckargs.iteritems():
                cvalue = cls.request.arguments.get(cname)
                cvalue = to_plain(cvalue)

                def invalid_recorder(msg):
                    diff = set(cls.request.arguments.keys()).symmetric_difference(set(ckargs.keys()))
                    cls.recorder('WARN', 'Check Arguements Invalid,{msg},[{diff}]'.format(msg=msg, diff=to_plain(diff)))
                    cls.end('ARG')

                if cvalue:
                    if ctype is int:
                        if not cvalue.isdigit():
                            invalid_recorder('{name} Type Error'.format(name=cname))
                            return
                    elif not isinstance(cvalue, ctype):
                        invalid_recorder('{name} Type Error'.format(name=cname))
                        return 
                else:
                    if isinstance(cls, Api):
                        invalid_recorder('{name} Empty'.format(name=cname))
                        return 
                    elif isinstance(cls, Page):
                        invalid_recorder('{name} Empty'.format(name=cname))
                        return 
                cls.request.arguments[cname] = ctype(cvalue)
            return fn(cls, *args, **kwargs)
        return _wrap
    return _deco


def catchError(fn):
    """异常处理"""

    def _deco(cls, *args, **kwargs):
        try:
            return fn(cls, *args, **kwargs)
        except:
            cls.recorder('ERROR', '{message}'.format(message=traceback.format_exc()))
            if isinstance(cls, Api):
                cls.end('SVR')
            elif isinstance(cls, Page):
                cls.recorder('ERROR', '{message}'.format(message='错误页面'))
            return
    return _deco
