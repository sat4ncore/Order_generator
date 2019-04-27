import logging
import json

LOGGER = logging.getLogger("Order_generator.json")


class JsonFileService:
    @classmethod
    def read(cls, handle, binary=False):
        try:
            with open(handle, mode.Modes.READ) as file:
                return json.load(file)
        except IOError as ex:
            logger.Logger.error(ex)

