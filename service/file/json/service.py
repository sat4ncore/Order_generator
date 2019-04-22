import json
import config.constant.file.mode as mode
import util.logger.logger as logger


class JsonFileService:
    @classmethod
    def read(cls, handle):
        if isinstance(handle, str):
            try:
                with open(handle, mode.Modes.READ) as file:
                    return json.load(file)
            except IOError as ex:
                logger.Logger.error(ex)

