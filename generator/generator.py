import generator.builder.builder as builder
import service.reporter.reporter as reporter
import util.logger.logger as logger
import random


class OrderGenerator:
    def __init__(self, volume, chunk_size, red_zone, green_zone, blue_zone, generation):
        logger.Logger.info("Generator configuration...")
        self.__volume = volume
        self.__chunk_size = chunk_size
        self.__red_zone = red_zone * volume // 100
        self.__green_zone = green_zone * volume // 100
        self.__blue_zone = blue_zone * volume // 100
        self.__builder = builder.OrderBuilder(**generation)

    @reporter.Reporter.increment_red_zone
    def __generate_red_zone(self):
        orders = []
        build = self.__builder.build()
        for _ in range(random.randint(1, 2)):
            orders.append(next(build))
        return orders

    @reporter.Reporter.increment_green_zone
    def __generate_green_zone(self):
        orders = []
        build = self.__builder.build()
        for _ in range(3):
            orders.append(next(build))
        return orders

    @reporter.Reporter.increment_blue_zone
    def __generate_blue_zone(self):
        orders = []
        build = self.__builder.build()
        next(build)
        for _ in range(random.randint(1, 2)):
            orders.append(next(build))
        return orders

    def generate(self) -> list:
        order_record = None
        if self.__red_zone > 0:
            order_record = self.__generate_red_zone()
            self.__red_zone -= 1
        elif self.__green_zone > 0:
            order_record = self.__generate_green_zone()
            self.__green_zone -= 1
        elif self.__blue_zone > 0:
            order_record = self.__generate_blue_zone()
            self.__blue_zone -= 1
        return order_record

    def generate_many(self):
        logger.Logger.debug(f"Generation of a chunk with a size {self.__chunk_size}...")
        for _ in range(self.__chunk_size):
            yield self.generate()
