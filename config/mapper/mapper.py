import dataclasses


@dataclasses.dataclass(frozen=True)
class ConfigMapper:
    Generator: dict
    Logger: dict
    MySQL: dict
    RabbitMQ: dict
    Publisher: dict
