from dataclasses import dataclass
from collections import namedtuple


@dataclass(frozen=True)
class OrderData:
    """
    This class does not support insertion into MySQL without conversions.
    """
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


"""
Solving an insert problem without a builder architecture change
"""
OrderTuple = namedtuple("OrderTuple", "identifier currency_pair direction status timestamp initial_price "
                                      "filled_price initial_volume filled_volume description tags")
