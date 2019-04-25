import dataclasses


@dataclasses.dataclass(frozen=True)
class Order:
    identifier: str
    currency_pair: str
    direction: str
    status: str
    timestamp: str
    initial_price: float
    filled_price: float
    initial_volume: float
    filled_volume: float
    description: str
    tags: str

    def __iter__(self):
        for field in self.__dict__.values():
            yield field
