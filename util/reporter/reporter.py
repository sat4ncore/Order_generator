from config.constant.reporter import ReportConstant
from config.constant.module import Module
import logging
import time

LOGGER = logging.getLogger(Module.REPORTER)


class Reporter:
    _statistics = {
        ReportConstant.RED_ZONE: 0,
        ReportConstant.GREEN_ZONE: 0,
        ReportConstant.BLUE_ZONE: 0,
        ReportConstant.FROM_RABBIT_MQ: 0,
        ReportConstant.INTO_MYSQL: 0
    }
    _time_statistics = {
        ReportConstant.GENERATING: 0,
        ReportConstant.INTO_MYSQL: 0,
        ReportConstant.PUBLISHING: 0
    }

    @classmethod
    def update_time(cls, func):
        def wrapper(*args, **kwargs):
            now = time.time()
            result = func(*args, **kwargs)
            cls._time_statistics[func.__name__] += time.time() - now
            return result
        return wrapper

    @classmethod
    def update_statistics(cls, func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            cls._statistics[func.__name__] += 1
            return result
        return wrapper

    @classmethod
    def update_insertion(cls, func):
        def _execute_many(*args, **kwargs):
            result = func(*args, **kwargs)
            cls._statistics[func.__name__] += result
            return result

        return _execute_many

    @classmethod
    def report(cls):
        LOGGER.info("""
=================================================
          Order generator by sat4ncore
=================================================
                   Generated
Red zone = %s
Green zone = %s
Blue zone = %s
Time = %s

                   RabbitMQ
Received = %s
Publish time = %s

                    MySQL
Saved = %s
Time = %s
=================================================""",
                    cls._statistics[ReportConstant.RED_ZONE],
                    cls._statistics[ReportConstant.GREEN_ZONE],
                    cls._statistics[ReportConstant.BLUE_ZONE],
                    round(cls._time_statistics[ReportConstant.GENERATING], 3),
                    cls._statistics[ReportConstant.FROM_RABBIT_MQ],
                    round(cls._time_statistics[ReportConstant.PUBLISHING], 3),
                    cls._statistics[ReportConstant.INTO_MYSQL],
                    round(cls._time_statistics[ReportConstant.INTO_MYSQL], 3))
