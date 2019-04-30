from config.constant.file_mode import READ
import logging

LOGGER = logging.getLogger(__name__)


class TextFileService:
    @classmethod
    def read_all(cls, handle):
        if isinstance(handle, str):
            try:
                with open(handle, READ) as file:
                    return file.read()
            except IOError as ex:
                LOGGER.error(ex)

    @classmethod
    def read_lines(cls, handle):
        if isinstance(handle, str):
            try:
                with open(handle, READ) as file:
                    return file.readlines()
            except IOError as ex:
                LOGGER.error(ex)
