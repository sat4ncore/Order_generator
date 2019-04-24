import mysql.connector as mysql


class MySQLService:
    def __init__(self):
        self._connection = None

    mysql.connect