import dataclasses
import random
import config.constant.generator.const as const
import time
import entity.order.order as order


@dataclasses.dataclass(frozen=True)
class OrderBuilder:
    random_seed: int
    identifier_bit_depth: int
    currency_pairs: list
    descriptions: list
    tags: list
    tags_in_order: int
    unique_identifiers: set = dataclasses.field(default_factory=set)
    currency_prices: dict = dataclasses.field(default_factory=dict)
    initial_timestamp: int = int(time.time() * 10 ** 3)

    def __post_init__(self):
        random.seed(self.random_seed)
        self.currency_prices.update(zip(self.currency_pairs,
                                        [round(random.uniform(0, 100), 5) for _ in self.currency_pairs]))

    def build(self):
        identifier = 0
        exists = True
        while exists:
            identifier = random.randrange(10 ** (self.identifier_bit_depth - 1), 10 ** self.identifier_bit_depth)
            if identifier not in self.unique_identifiers:
                exists = False
        currency_pair = random.choice(self.currency_pairs)
        direction = random.choice(const.GeneratorConsts.DIRECTIONS)
        timestamp = self.initial_timestamp + random.randrange(const.GeneratorConsts.WEEK_TIMESTAMP)
        timestamp += random.randint(1000, 5000)
        initial_price = self.currency_prices[currency_pair]
        initial_volume = round(random.random() * 10 ** 5, 8)
        description = random.choice(self.descriptions)
        tags = ", ".join(random.sample(self.tags, random.randint(1, self.tags_in_order)))

        yield order.Order(identifier, currency_pair, direction, const.GeneratorConsts.STATUS_NEW,
                          timestamp, initial_price, 0, initial_volume, 0., description, tags)

        timestamp += random.randint(1000, 5000)

        yield order.Order(identifier, currency_pair, direction, const.GeneratorConsts.STATUS_TO_PROVIDER,
                          timestamp, initial_price, 0., initial_volume, 0., description, tags)

        timestamp += random.randint(1000, 5000)

        status = random.choice(const.GeneratorConsts.FINAL_STATUSES)

        percent = random.uniform(0.95, 1.05)
        final_order = {
            const.GeneratorConsts.STATUS_REJECT: order.Order(identifier, currency_pair, direction, status, timestamp,
                                                             initial_price, 0., initial_volume, 0., description, tags),
            const.GeneratorConsts.STATUS_FILLED: order.Order(identifier, currency_pair, direction, status, timestamp,
                                                             initial_price, initial_price, initial_volume,
                                                             initial_volume, description, tags),
            const.GeneratorConsts.STATUS_PARTIAL_FILLED: order.Order(identifier, currency_pair, direction, status,
                                                                     timestamp, initial_price,
                                                                     round(initial_price * percent, 5),
                                                                     initial_volume, round(initial_volume * percent, 8),
                                                                     description, tags)
        }

        yield final_order[status]
