import util.pattern.singleton as single
import logging
import logging.config
import config.constant.logger.const as consts
import config.constant.logger.level as levels


class Logger(metaclass=single.SingletonMeta):
    _logger = logging.getLogger(consts.LoggerConsts.MAIN_MODULE)

    def __init__(self, dict_log_config=None):
        if dict_log_config:
            logging.config.dictConfig(dict_log_config)
        else:
            logging.basicConfig(format=consts.LoggerConsts.DEFAULT_FORMAT,
                                level=logging.INFO)
        logging.getLogger("pika").propagate = False
        self._logger.info("Logger successfully configured")

    @classmethod
    def info(cls, message):
        cls._logger.info(message)

    @classmethod
    def debug(cls, message):
        cls._logger.debug(message)

    @classmethod
    def warning(cls, message):
        cls._logger.warning(message)

    @classmethod
    def error(cls, ex):
        cls._logger.error(ex)

    @classmethod
    def fatal(cls, ex, code):
        cls._logger.fatal(ex)
        exit(code)
