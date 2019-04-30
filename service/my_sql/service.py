from config.constant.exit_code import ExitCode
from config.constant.module import ModuleName
import mysql.connector
import logging

LOGGER = logging.getLogger(ModuleName.MYSQL_SERVICE)


class MySQLService:
    def __init__(self):
        self._connection = None

    def _open(self, host, port, user, password, database, pool_name, pool_size):
        self._connection = mysql.connector.connect(pool_name, pool_size, host=host, port=port,
                                                   user=user, password=password, database=database)

    def open(self, user, password, database, host="localhost", port=3306, pool_name=None, pool_size=None):
        try:
            LOGGER.info("Attempting to open connection with MySQL")
            self._open(host, port, user, password, database, pool_name, pool_size)
        except mysql.connector.ProgrammingError as ex:
            LOGGER.fatal(ex)
            exit(ExitCode.MYSQL)


"""
class MySqlService:
    def __init__(self):
        self._connection: mysql.connector.MySQLConnection = None


    def _execute(self, cursor, query, params):
        logger.Logger.debug('Executing query: {}'.format(query % params))
        cursor.execute(query, params)

    def _reconnect(self):
        logger.Logger.info("Reconnection...")
        self._connection.reconnect(10, 1)

    def execute(self, query, params=(), multi=False):
        try:
            cursor = self._connection.cursor()
            if multi:
                for item in params:
                    self._execute(cursor, query, item)
            else:
                cursor.execute(query, params)
            self._connection.commit()
        except mysql.connector.Error as err:
            logger.Logger.error(err.msg)
            self._reconnect()
            self.execute(query, params, multi)

    def _execute_many(self, params, queries):
        cursor = self._connection.cursor()

        cursor.executemany(params, queries)
        self._connection.commit()

    def execute_many(self, params, queries):
        try:
            logger.Logger.debug('Executing many queries started')
            for o in queries:
                print(o)
            self._execute_many(params, queries)
        except mysql.connector.Error as ex:
            logger.Logger.error(ex)
            self._reconnect()
            self._execute_many(params, queries)

    def close(self):
        logger.Logger.debug('Closing MySQL connection')
        self._connection.close()

    def open(self, user, password, host, port, database):
        try:
            logger.Logger.info('Opening MySQL connection')
            self._connection = mysql.connector.connect(user=user, password=password, host=host, port=port, database=database)
        except mysql.connector.errors.Error as e:
            logger.Logger.fatal(e, code.ExitCode.MYSQL)
"""
