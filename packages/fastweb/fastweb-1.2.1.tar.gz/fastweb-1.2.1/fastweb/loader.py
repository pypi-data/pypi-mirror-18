# coding:utf-8

from fastweb.manager import Manager
from fastweb.utils.base import Configer
from fastweb.utils.log import get_logger


class Loader(object):
    """加载器"""

    def __init__(self):
        self.config = {}
        self.config_handler = None

        self.err_code = {}

        self.mime = {}
        self.manager = None

        self.logger = None
        self.request_logger = None

    def load_config(self, config_path):
        configer = Configer(config_path)
        self.config_handler = configer
        self.config = configer.config

    def load_err_code(self):
        err_code = {
            'SUC': {'code': 0, 'message': 'success'},
            'ARG': {'code': 1001, 'message': 'invalid arguments'},
            'SVR': {'code': 2001, 'message': '服务器错误'},
            'TOKEN': {'code': 3995, 'message': 'Token失效'},
            'KEY': {'code': 4001, 'message': 'key not exist'},
            'EXT': {'code': 4002, 'message': 'key exist'},
            'PWD': {'code': 4003, 'message': 'password wrong'},
            'FMT': {'code': 4004, 'message': 'format error'},
            'FT': {'code': 4005, 'message': 'upload file type not support'},
        }

        self.err_code = err_code

    def load_mime(self):
        mime = {
            'image/gif': '.gif',
            'image/x-png': '.png',
            'image/x-jpeg': '.jpeg',
            'image/jpeg': '.jpeg',
            'image/png': '.png'
        }

        self.mime = mime

    def load_manager(self, asyn=True):
        self.manager = Manager(asyn=asyn)

    def load_logger(self, path):
        self.logger = get_logger(path, request=False)
        self.logger.propagate = False
        self.request_logger = get_logger(path, request=True)
        self.request_logger.propagate = False

gl = Loader()
