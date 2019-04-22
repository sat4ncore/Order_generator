import util.pattern.singleton as single
import logging
import logging.config
import config.constant.logger.const as consts
import config.constant.logger.level as levels


class Logger(metaclass=single.SingletonMeta):
    # TODO: add different logging levels for each module
    logger = logging.getLogger(consts.LoggerConsts.MAIN_MODULE)

    def __init__(self, dict_log_config=None):
        if dict_log_config:
            logging.config.dictConfig(dict_log_config)
        else:
            logging.basicConfig(format=consts.LoggerConsts.DEFAULT_FORMAT,
                                level=levels.LogLevels.WARNING)

    @classmethod
    def info(cls, message):
        cls.logger.info(message)

    @classmethod
    def debug(cls, message):
        cls.logger.debug(message)

    @classmethod
    def warning(cls, message):
        cls.logger.warning(message)

    @classmethod
    def error(cls, ex, raw=True):
        cls.logger.error(ex)
        if raw:
            raise ex

    @classmethod
    def fatal(cls, ex):
        cls.logger.fatal(ex)
        raise ex
