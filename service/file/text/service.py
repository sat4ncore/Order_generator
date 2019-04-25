import config.constant.file.mode as mode
import util.logger.logger as logger


class TextFileService:
    @classmethod
    def read(cls, handle):
        if isinstance(handle, str):
            try:
                with open(handle, mode.Modes.READ) as file:
                    return file.read()
            except IOError as ex:
                logger.Logger.error(ex)

    @classmethod
    def readlines(cls, handle):
        if isinstance(handle, str):
            try:
                with open(handle, mode.Modes.READ) as file:
                    return file.readlines()
            except IOError as ex:
                logger.Logger.error(ex)
