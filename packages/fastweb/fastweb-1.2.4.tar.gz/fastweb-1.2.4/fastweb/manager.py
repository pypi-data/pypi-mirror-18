# coding:utf-8

import fastweb.loader
from fastweb.utils.log import get_logger
from fastweb.exception import ConfigError
from fastweb import coroutine, Return, gen
from fastweb.component.db.fmysql import (AsynMysql, Mysql)
from fastweb.component.db.fredis import (AsynRedis, Redis)
from fastweb.component.db.fmongo import (AsynMongo, Mongo)
from fastweb.component.rpc.fthrift import (AsynRpc, Rpc)
from fastweb.component import (USED, IDLE, ERROR)

ASYN = 'asyn'
POOL_SIZE = 20
ASYN_MANAGER_TUPLE = [('mysql', AsynMysql, POOL_SIZE),
                      ('redis', AsynRedis, POOL_SIZE),
                      ('mongo', AsynMongo, POOL_SIZE),
                      ('rpc', AsynRpc, POOL_SIZE)]
MANAGER_TUPLE = [('mysql', Mysql, POOL_SIZE),
                 ('redis', Redis, POOL_SIZE),
                 ('mongo', Mongo, POOL_SIZE),
                 ('rpc', Rpc, POOL_SIZE)]

logger = get_logger(__name__)
logger.propagate = False


class Manager(object):
    """组件管理器
       组件名称不可以重复"""

    _managers = {}

    def __init__(self, asyn=True):
        self._logger = None
        self.asyn = asyn
        self.reset()

    def set_logger(self, logfunc):
        self._logger = logfunc

    def reset(self):
        """组件初始化"""

        if fastweb.loader.gl.config_handler:
            for (cpre, cls, num) in ASYN_MANAGER_TUPLE if self.asyn else MANAGER_TUPLE:
                components = fastweb.loader.gl.config_handler.get_components(cpre)

                for name, value in components.items():
                    config = fastweb.loader.gl.config[name]
                    max = int(config.get('max', num))
                    pool = []

                    if config:
                        if value['object'] in self._managers.keys():
                            logger.debug(
                                'Config Section[{}] Duplicate!'.format(
                                    value['object']))
                            continue
                        for x in range(max):
                            obj = cls(**config)
                            obj.name = value['object']
                            pool.append(obj)
                            logger.debug(
                                'Component Create Successful {obj}'.format(
                                    obj=obj))
                        if self.asyn:
                            self._managers['{name}_{asyn}'.format(name=value['object'], asyn=ASYN)] = (cls, config, pool)
                        else:
                            self._managers['{name}'.format(name=value['object'])] = (cls, config, pool)

            logger.debug('Component Pool Init Successful')

    def remove_component(self, name, component):
        try:
            self._managers[name].remove(component)
        except ValueError:
            logger.warn('[{component} not in Manager'.format(component=component))

    def __getattr__(self, name):
        """获取组件
           返回一个状态正常的组件,如果没有状态正常组件返回None"""

        name = '{name}_{asyn}'.format(name=name, asyn=ASYN) if self.asyn else name
        cls, config, components = self._managers.get(name, (None, None, None)) 

        if cls and config:
            for component in components:
                if component.status == IDLE:
                    component.set_used(self._logger)
                    return component
                elif component.status == ERROR:
                    self._logger('WARN', '[{cls}] component error [{message}],try rebuilding'.format(cls=cls.__name__, message=component.message))
                    component.rebuild()
                    component.set_used(self._logger)
                    return component

            self._logger('WARN', '[{cls}] Pool exhaust'.format(cls=cls.__name__))
            component = cls(**config)

            if component.status == IDLE:
                self._managers[name][2].append(component)
                component.set_used(self._logger)
                return component
            else:
                return None
        else:
            return None
