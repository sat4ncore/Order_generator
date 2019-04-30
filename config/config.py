from dataclasses import dataclass


@dataclass(frozen=True)
class ProjectConfig:
    Generator: dict
    Publisher: dict
    RabbitMQ: dict
    MySQL: dict
