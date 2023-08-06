# *-* coding:utf-8 *-*

import MySQLdb 
import tornado_mysql
from tornado import iostream
from tornado.locks import Condition

from fastweb import ioloop
import fastweb.utils.tool as tool
from fastweb.utils.log import get_logger
from fastweb.exception import MysqlError
from fastweb import coroutine, Return, gen
from fastweb.component import BaseComponent

logger = get_logger(__name__)

DEFAULT_PORT = 3306
DEFAULT_TIMEOUT = 5
DEFAULT_RETRY_TIMES = 3
DEFAULT_AUTOCOMMIT = True
DEFAULT_CHARSET = 'utf8'

class Mysql(BaseComponent):
    """同步mysql"""

    def __init__(self,**args):
        self._connect_flag = False

        self._cur = None
        self._conn = None
        self._sql = ''
        self._retry = DEFAULT_RETRY_TIMES
        self._query_list = []

        self._mysql_config = args
        self.reset(args)

    def reset(self,args):
        self.set_idle()
        mysql_config = {'host':args['host'],'port':int(args['port']),'user':args['user'],'db':args['db'],
                        'passwd':args['password'],'charset':args.get('charset'),'connect_timeout':int(args.get('timeout'))}

        #status: 0 free;1 used;
        self._status = 0
        self._event_flag = False
        
        if self._connect_flag:
            self._cur.close()
            self._conn.close() 

        try:
            self._conn = MySQLdb.connect(**mysql_config)
            self._cur = self._conn.cursor(MySQLdb.cursors.DictCursor)
            self._connect_flag = True

        except MySQLdb.Error,e:
            self._connect_flag = False
            self._logger('ERROR', 'Mysql Error -- msg[Connect Failed]')
            raise MysqlError('Connect Failed')

    def start_event(self):
        try:
            self._conn.autocommit(False)
            self._conn.begin()
            self._event_flag = True

        except MySQLdb.OperationalError,e:
            self.reconnect()
            self.start_event()

    def exec_event(self,sql,**kwds):
        if self._event_flag:
            res = self.query(sql,**kwds)
            return res

        else:
            self.logger('ERROR', 'Mysql Error -- [Not Start Event]')
            raise MysqlError('Not Start Event')

    def end_event(self):
        if self._event_flag:
            self._conn.commit()
            self._conn.autocommit(True)
            self._event_flag = False

    def query(self,sql,**kwds):
        for i in range(self._retry):
            try:
                kwds = {k:self._sql_str(v) for k,v in kwds.iteritems()}
                self._kwds = kwds
                self._sql = sql = sql.format(**kwds)
                with tool.timing('s', 10) as t:
                    self._cur.execute(sql)  
                self._query_list.append(self._sql)
                self._sql = ''
            except MySQLdb.OperationalError,e:
                self.reconnect()
                self._logger('ERROR', 'Mysql Error -- SQL[%s] -- msg[Mysql Gone Away or Operate Error!%s]' % (sql,e))
                continue
            except MySQLdb.Error,e:
                self._event_flag = False
                self._logger('ERROR', 'Mysql Error -- SQL[%s] -- msg[Mysql Execute Failed!%s] -- query list[%s]' % (sql,e, self._query_list))
                raise MysqlError('Mysql Execute Failed')
            except:
                self._logger('ERROR', 'Mysql Error -- msg[Sql Format Failed!] -- SQL[%s] -- Data[%s]' % (sql,kwds))
                raise MysqlError('Sql Format Failed')
                
            effect = self._cur.rowcount
            self._logger('INFO', 'Mysql Sql [{sql}] -- [{row}] -- [{time}]'.format(sql=sql, row=effect, time=t))

            if not self._event_flag:
                self._conn.commit()

            return effect
        
        raise MysqlError('Mysql Gone Away or Operate Error')

    def _sql_str(self, v):
        if v is None:
            return 'Null'
        return v

    def reconnect(self):
        self.reset(self._mysql_config)
        self._logger('INFO', 'Mysql Reconnect')

    def rollback(self):
        self._conn.rollback()

    def fetch(self):
        return self._cur.fetchone()

    def fetchall(self):
        return self._cur.fetchall()

    def commit(self):
        self._conn.commit()

    @property
    def id(self):
        return int(self._conn.insert_id())

    @property
    def sql(self):
        return self._sql

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self,status):
        self._status = status    

    def __def__(self):
        self._cur.close()
        self._conn.close()

class AsynMysql(BaseComponent):
    """异步mysql组件"""

    def __init__(self, **kwargs):
        super(AsynMysql, self).__init__()
        self._connect_flag = False
        self._cur = None
        self._conn = None
        self.sql = ''
        self._connect_condition = Condition()

        self.mysql_config = kwargs
        self.rebuild(kwargs)

    def __str__(self):
        return '<AsynMysql {host} {port} {user} {db} {name} {charset}>'.format(
            host=self.host,
            port=self.port,
            user=self.user,
            db=self.db,
            name=self.name,
            charset=self.charset)

    @property
    def id(self):
        return int(self._conn.insert_id())

    @coroutine
    def rebuild(self, kwargs):
        self.host = kwargs.get('host')
        assert self.host, '`host` is essential of mysql'
        self.port = kwargs.get('port', DEFAULT_PORT)
        self.user = kwargs.get('user', '')
        self.password = kwargs.get('password', '')
        self.db = kwargs.get('db')
        self.charset = kwargs.get('charset', DEFAULT_CHARSET)
        self.timeout = kwargs.get('timeout', DEFAULT_TIMEOUT)
        self.autocommit = kwargs.get('autocommit', DEFAULT_AUTOCOMMIT)

        self.mysql_config = {'host': self.host,
                             'port': int(self.port),
                             'user': self.user,
                             'passwd': self.password,
                             'charset': self.charset,
                             'connect_timeout': int(self.timeout),
                             'autocommit': self.autocommit}

        if self.db:
            self.mysql_config['db'] = self.db

        self._event_flag = False

        # 确认是否已经建立连接
        if self._connect_flag:
            self.close()
        try:
            self.set_idle()
            self._conn = yield tornado_mysql.connect(**self.mysql_config)
            self._cur = self._conn.cursor(tornado_mysql.cursors.DictCursor)
            self._connect_condition.notify()
            self._connect_flag = True
        except tornado_mysql.Error as ex:
            self._connect_flag = False
            self.set_error(ex)


    def start_event(self):
        """开始事务"""

        try:
            self._conn.autocommit(False)
            self._conn.begin()
            self._event_flag = True
        except tornado_mysql.OperationalError as ex:
            self._logger('WARN', 'Mysql Reconnect [{message}]'.format(message=ex))
            self.reconnect()
            self.start_event()

    def exec_event(self, sql, **kwargs):
        """执行事务"""

        if self._event_flag:
            res = self.query(sql, **kwargs)
            return res
        else:
            self._logger('ERROR', 'Mysql Exec Event [Not Start Event]')
            raise MysqlError

    def end_event(self):
        """结束事务"""

        if self._event_flag:
            self._conn.commit()
            self._conn.autocommit(True)
            self._event_flag = False

    @coroutine   
    def query(self, sql, **kwds):
        """执行sql"""

        t = 0

        for i in range(DEFAULT_RETRY_TIMES):
            try:
                kwds = {k:self._sql_str(v) for k,v in kwds.iteritems()}
                self._kwds = kwds
                self._sql = sql = sql.format(**kwds)

                if not self._cur:
                    yield self._connect_condition.wait()
                with tool.timing('s', 10) as t:
                    yield self._cur.execute(sql)
                
                self.sql = ''
            #连接断开或cursor断开
            except (iostream.StreamClosedError, tornado_mysql.ProgrammingError, tornado_mysql.InternalError) as ex:
                self.reconnect()
                self._logger(
                    'ERROR', 'Mysql Error [{sql}] -- [{message}]'.format(sql=sql, message=ex))
                continue
            #执行sql语句错误
            except (tornado_mysql.IntegrityError, tornado_mysql.OperationalError) as ex:
                self._event_flag = False
                self._logger(
                    'ERROR', 'Mysql Error [{sql}] -- [{message}]'.format(sql=sql, message=ex))
                raise MysqlError('Mysql Execute Failed')
            except KeyError, TypeError:
                self._logger(
                    'ERROR', 'Mysql Error [{sql}] -- [{data}]'.format(
                    sql=sql, data=kwds))
                raise MysqlError('Sql Format Failed')

            effect = self._cur.rowcount
            self._logger('INFO', 'Mysql Sql [{sql}] -- [{row}] -- [{time}]'.format(sql=sql, row=effect, time=t))

            if not self._event_flag:
                yield self._conn.commit()

            raise Return(effect)

        self._logger('ERROR', 'Mysql Connect Error')
        raise MysqlError

    def _sql_str(self, v):
        if v is None:
            return 'Null'
        return v

    def reconnect(self):
        """重连"""

        self.rebuild(self.mysql_config)
        self.recorder('INFO', 'Mysql Reconnect!')

    @coroutine
    def rollback(self):
        """回滚"""

        yield self._conn.rollback()

    def fetch(self):
        """获取单条数据"""

        return self._cur.fetchone()

    def fetchall(self):
        """获取多条数据"""

        return self._cur.fetchall()

    @coroutine
    def commit(self):
        """提交操作"""

        yield self._conn.commit()
    
    @coroutine
    def close(self):
        """关闭连接"""

        yield self._cur.close()
        yield self._conn.close()

    def __def__(self):
        self.close()
