from dataclasses import dataclass


@dataclass(frozen=True)
class ProjectConfig:
    Generator: dict
    Exchange: dict
    RabbitMQ: dict
    MySQL: dict
