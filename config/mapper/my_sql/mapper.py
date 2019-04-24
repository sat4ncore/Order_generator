import dataclasses


@dataclasses.dataclass(frozen=True)
class MySQLConfigMapper:
    host: str
    port: int
    user: str
    password: str
    database: str
