from dataclasses import dataclass


@dataclass(frozen=True)
class ExchangeConfig:
    exchange: str
    exchange_type: str
