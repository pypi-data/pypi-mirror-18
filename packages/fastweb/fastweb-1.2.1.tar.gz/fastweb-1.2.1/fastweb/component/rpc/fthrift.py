# coding:utf8

import six
import sys
from thrift import TTornado
from tornado.locks import Condition
from importlib import import_module
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from tornado.gen import coroutine, Return

from fastweb.exception import RpcError
from fastweb.utils.log import get_logger
from fastweb.component import BaseComponent

logger = get_logger(__name__)


class Rpc(BaseComponent):

    def __init__(self, **kvargs):
        self.reset(kvargs)

    def reset(self, kvargs):
        self.status = 0
        host = kvargs.get('host')
        assert host, 'rpc config must have host'
        port = int(kvargs.get('port'))
        assert port, 'rpc config must have port'
        service_name = kvargs.get('service_name')
        assert service_name, 'rpc config must have service_name'
        module = kvargs.get('module')
        assert module, 'rpc config must have service module'

        if isinstance(module, six.string_types):
            module = import_module(module)

        self.connect(host, port, service_name, module)


    def connect(self, host, port, service_name, module):
        transport = TSocket.TSocket(host, port)
        self._transport = TTransport.TBufferedTransport(transport)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        pfactory = TMultiplexedProtocol.TMultiplexedProtocol(protocol, service_name)
        self._transport.open()
        self.client = getattr(module, 'Client')(pfactory)

    def __getattr__(self, name):
        if hasattr(self.client, name):
            return getattr(self.client, name)

    def close(self):
        self.transport.close()


class AsynRpc(BaseComponent):
    """thrift RPC组件"""

    def __init__(self, **kvargs):
        super(AsynRpc, self).__init__()
        self.rebuild(kvargs)

    def __str__(self):
        return '<AsynThrift Rpc {host} {port} {module_path} {module} {name}>'.format(
            host=self.host,
            port=self.port,
            module_path=self.thrift_module_path,
            module=self.thrift_module,
            name=self.name)

    def rebuild(self, kvargs):
        self.client = None
        self.host = kvargs.get('host')
        assert self.host, 'host is essential of rpc'
        self.port = int(kvargs.get('port'))
        assert self.port, 'port is essential of rpc'
        self.thrift_module_path = kvargs.get('thrift_module_path')
        assert self.thrift_module_path, 'thrift_module_path is essential of rpc'
        self.thrift_module = kvargs.get('thrift_module')
        assert self.thrift_module, 'thrift_module is essential of rpc'

        sys.path.append(self.thrift_module_path)

        if isinstance(self.thrift_module, six.string_types):
            self.module = import_module(self.thrift_module)

        self.transport = TTornado.TTornadoStreamTransport(self.host, self.port)

        try:
            self.set_idle()
            self.transport.open()
        except TTransport.TTransportException as ex:
            self.set_error(ex)
        
        protocol = TBinaryProtocol.TBinaryProtocolFactory()
        self.client = getattr(self.module, 'Client')(self.transport, protocol)

    def __getattr__(self, name):
        if hasattr(self.client, name):
            callable = getattr(self.client, name)
            return callable

    def close(self):
        if self.transport:
            self.transport.close()

