MAIN = "Order_generator"


class Module:
    _MAIN_SUB_FORMAT = f"{MAIN}.%s"
    BUILDER = _MAIN_SUB_FORMAT % "Builder"
    GENERATOR = _MAIN_SUB_FORMAT % "Generator"
    REPORTER = _MAIN_SUB_FORMAT % "Reporter"


class MySQLModule:
    _SUB_FORMAT = f"{MAIN}.MySQL.%s"
    CONNECTION = _SUB_FORMAT % "Connection"
    SERVICE = _SUB_FORMAT % "Service"


class RabbitMQModule:
    _SUB_FORMAT = f"{MAIN}.RabbitMQ.%s"
    CONNECTION = _SUB_FORMAT % "Connection"
    CONSUMER = _SUB_FORMAT % "Consumer"
    PUBLISHER = _SUB_FORMAT % "Publisher"
    SERVICE = _SUB_FORMAT % "Service"
