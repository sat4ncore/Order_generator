from config.constant.reporter import ReportConstant
from config.constant.module import Module
import logging

LOGGER = logging.getLogger(Module.REPORTER)


class Reporter:
    _statistics = {
        ReportConstant.RED_ZONE: 0,
        ReportConstant.GREEN_ZONE: 0,
        ReportConstant.BLUE_ZONE: 0,
        ReportConstant.FROM_RABBIT_MQ: 0,
        ReportConstant.INTO_MYSQL: 0
    }

    @classmethod
    def update_statistics(cls, func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            cls._statistics[func.__name__] += 1
            return result
        return wrapper

    @classmethod
    def update_insertion(cls, func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            cls._statistics[func.__name__] += result
            return result

        return wrapper

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

                   RabbitMQ
Received = %s

                    MySQL
Saved = %s
=================================================""",
                    cls._statistics[ReportConstant.RED_ZONE],
                    cls._statistics[ReportConstant.GREEN_ZONE],
                    cls._statistics[ReportConstant.BLUE_ZONE],
                    cls._statistics[ReportConstant.FROM_RABBIT_MQ],
                    cls._statistics[ReportConstant.INTO_MYSQL])
