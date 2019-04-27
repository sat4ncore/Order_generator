class _RabbitMQModule:
    MAIN = "RabbitMQ"
    _SUB_FORMAT = f"{MAIN}.%s"
    CONNECTION = _SUB_FORMAT % "Connection"
    CONSUMER = _SUB_FORMAT % "Consumer"
    PUBLISHER = _SUB_FORMAT % "Publisher"
    SERVICE = _SUB_FORMAT % "Service"


class _MySQLModule:
    MAIN = "MySQL"
    _SUB_FORMAT = f"{MAIN}.%s"
    CONNECTION = _SUB_FORMAT % "Connection"
    SERVICE = _SUB_FORMAT % "Service"


class ModuleName:
    MAIN = "Order_generator"
    _SUB_FORMAT = f"{MAIN}.%s"
    BUILDER = _SUB_FORMAT % "Builder"
    GENERATOR = _SUB_FORMAT % "Generator"
    REPORTER = _SUB_FORMAT % "Reporter"
    RMQ = _RabbitMQModule
    MYSQL = _MySQLModule
