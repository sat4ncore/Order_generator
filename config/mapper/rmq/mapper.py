import dataclasses


@dataclasses.dataclass(frozen=True)
class RabbitMQConfigMapper:
    host: str
    port: int
    virtual_host: str
    user: str
    password: str
    exchange_type: str
    exchange_name: str


@dataclasses.dataclass(frozen=True)
class RabbitMQPublisherMapper:
    exchange: str
    exchange_type: str
