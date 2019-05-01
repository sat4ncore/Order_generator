from util.serializer.protobuf.serializer import ProtobufSerializer
from service.mysql.service import MySQLService
from config.constant.mysql import INSERT_ORDER
from config.constant.module import Module
import threading
import logging
import time

LOGGER = logging.getLogger(Module.REPORTER)


class OrderCollector(threading.Thread):
    _collection = []
    _lock = threading.Lock()

    def __init__(self, my_sql):
        super(OrderCollector, self).__init__()
        self._my_sql: MySQLService = my_sql
        self._stop_event = False

    @classmethod
    def collect(cls, func):
        def wrapper(*args, **kwargs):
            result = ProtobufSerializer.deserialize(func(*args, **kwargs))
            cls._lock.acquire()
            cls._collection.append(result)
            cls._lock.release()
            return result
        return wrapper

    def stop(self):
        self._stop_event = True

    def run(self):
        while not self._stop_event:
            time.sleep(5)
            if len(self._collection) > 0:
                LOGGER.info("Batch ready to execute")
                self._lock.acquire()
                self._my_sql.execute_many(INSERT_ORDER, self._collection)
                self._collection.clear()
                self._lock.release()
                LOGGER.info("Batch successfully executed")

