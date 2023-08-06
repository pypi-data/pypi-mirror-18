# coding:utf8

import six
from importlib import import_module
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.protocol import TMultiplexedProtocol

class RPC(object):

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

    def __del__(self):
        self.close()

