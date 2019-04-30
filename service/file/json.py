from config.constant.file_mode import READ
import logging
import json

LOGGER = logging.getLogger("Order_generator.json")


class JsonFileService:
    @classmethod
    def read(cls, handle):
        try:
            with open(handle, READ) as file:
                return json.load(file)
        except IOError as ex:
            LOGGER.error(ex)

