from config.constant.exit_code import GENERATOR as GENERATOR_EXIT
from config.constant.module import Module
from util.reporter.reporter import Reporter
from generator.builder import OrderBuilder
import logging
import random

LOGGER = logging.getLogger(Module.GENERATOR)


class OrderGenerator:
    def __init__(self, volume, chunk_size, red_zone, green_zone, blue_zone, builder):
        LOGGER.info("Generator configuration...")
        self._volume = volume
        if not isinstance(builder, OrderBuilder):
            LOGGER.error("Expected instance builder")
            exit(GENERATOR_EXIT)
        self._builder = builder
        if chunk_size > volume:
            LOGGER.warning("Incorrect chunk size specified")
        self._chunk_size = chunk_size
        if red_zone + green_zone + blue_zone != 100:
            LOGGER.error("The sum of the zones must be equal to 100")
            exit(GENERATOR_EXIT)
        self._red_zone = self._calculate_zone(red_zone)
        self._green_zone = self._calculate_zone(green_zone)
        self._blue_zone = self._calculate_zone(blue_zone)
        LOGGER.info("Configuration complete")

    def _calculate_zone(self, zone):
        return zone * self._volume // 100

    @Reporter.update_statistics
    def _generate_red_zone(self):
        orders = []
        build = self._builder.build()
        for _ in range(random.randint(1, 2)):
            orders.append(next(build))
        return orders

    @Reporter.update_statistics
    def _generate_green_zone(self):
        orders = []
        build = self._builder.build()
        for _ in range(3):
            orders.append(next(build))
        return orders

    @Reporter.update_statistics
    def _generate_blue_zone(self):
        orders = []
        build = self._builder.build()
        next(build)
        for _ in range(random.randint(1, 2)):
            orders.append(next(build))
        return orders

    def generate(self) -> list:
        order_record = None
        if self._red_zone > 0:
            order_record = self._generate_red_zone()
            self._red_zone -= 1
        elif self._green_zone > 0:
            order_record = self._generate_green_zone()
            self._green_zone -= 1
        elif self._blue_zone > 0:
            order_record = self._generate_blue_zone()
            self._blue_zone -= 1
        return order_record

    def generate_many(self):
        LOGGER.debug(f"Generation of a chunk with a size {self._chunk_size}...")
        for _ in range(self._chunk_size):
            yield self.generate()
