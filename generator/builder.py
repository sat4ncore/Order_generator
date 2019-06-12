from generator.order import OrderTuple as Order
from config.constant.order import Status, WEEK_TIMESTAMP, DIRECTIONS
from config.constant.module import Module
from dataclasses import dataclass, field
import logging
import random
import time

LOGGER = logging.getLogger(Module.BUILDER)


@dataclass(frozen=True)
class OrderBuilder:
    random_seed: int
    identifier_bit_depth: int
    currency_pairs: list
    descriptions: list
    tags: list
    tags_in_order: int
    unique_identifiers: set = field(default_factory=set)
    currency_prices: dict = field(default_factory=dict)
    initial_timestamp: int = int(time.time() * 10 ** 3)

    def __post_init__(self):
        LOGGER.info("Order builder configuration...")
        random.seed(self.random_seed)
        self.currency_prices.update(zip(self.currency_pairs,
                                        [round(random.uniform(0, 100), 5) for _ in self.currency_pairs]))
        LOGGER.info("Configuration complete")

    def build(self):
        identifier = 0
        exists = True
        while exists:
            identifier = random.randrange(10 ** (self.identifier_bit_depth - 1), 10 ** self.identifier_bit_depth)
            if identifier not in self.unique_identifiers:
                exists = False
        identifier = str(identifier)
        currency_pair = random.choice(self.currency_pairs)
        direction = random.choice(DIRECTIONS)
        timestamp = self.initial_timestamp + random.randrange(WEEK_TIMESTAMP)
        timestamp += random.randint(1000, 5000)
        initial_price = self.currency_prices[currency_pair]
        initial_volume = round(random.random() * 10 ** 5, 8)
        description = random.choice(self.descriptions)
        tags = ", ".join(random.sample(self.tags, random.randint(1, self.tags_in_order)))

        yield Order(identifier, currency_pair, direction, Status.NEW,
                    timestamp, initial_price, 0, initial_volume, 0., description, tags)

        timestamp += random.randint(1000, 5000)

        yield Order(identifier, currency_pair, direction, Status.TO_PROVIDER,
                    timestamp, initial_price, 0., initial_volume, 0., description, tags)

        timestamp += random.randint(1000, 5000)

        status = random.choice(Status.FINALS)

        filled_price = round(initial_price * random.uniform(0.95, 1.05), 5)
        final_order = {
            Status.REJECT: Order(identifier, currency_pair, direction, status, timestamp,
                                 initial_price, 0., initial_volume, 0., description, tags),
            Status.FILLED: Order(identifier, currency_pair, direction, status, timestamp,
                                 initial_price, initial_price, initial_volume,
                                 initial_volume / initial_price, description, tags),
            Status.PARTIAL_FILLED: Order(identifier, currency_pair, direction, status,
                                         timestamp, initial_price,
                                         filled_price,
                                         initial_volume, initial_volume / filled_price,
                                         description, tags)
        }

        yield final_order[status]
