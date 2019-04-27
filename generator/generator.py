from config.constant.module import ModuleName
from util.reporter import Reporter
import logging
import random

LOGGER = logging.getLogger(ModuleName.GENERATOR)


class OrderGenerator:
    def __init__(self, volume, chunk_size, red_zone, green_zone, blue_zone, builder):
        LOGGER.info("Generator configuration...")
        self._volume = volume
        self._chunk_size = chunk_size
        self._red_zone = self._calculate_zone(red_zone)
        self._green_zone = self._calculate_zone(green_zone)
        self._blue_zone = self._calculate_zone(blue_zone)
        self._builder = builder

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
        for record in self._builder.build():
            orders.append(next(record))
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
