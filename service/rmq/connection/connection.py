import pika
import pika.exceptions as exceptions
import util.logger.logger as logger
import config.constant.exit.code as code
import time


class RMQConnection:
    def __init__(self):
        self._connection: pika.BlockingConnection = None
        self._parameters = None

    def _open(self, host, port, virtual_host, user, password, connection_attempts):
        credentials = pika.PlainCredentials(user, password)
        self._parameters = pika.ConnectionParameters(host, port, virtual_host, credentials, connection_attempts)
        logger.Logger.info("Attempting to open connection to RabbitMQ...")
        self._connection = pika.BlockingConnection(self._parameters)
        logger.Logger.info("Connection to RabbitMQ successfully established")

    def open(self, host="localhost", port=5672, virtual_host="/", user="guest", password="guest",
             connection_attempts=30):
        try:
            self._open(host, port, virtual_host, user, password, connection_attempts)
        except exceptions.AMQPConnectionError:
            logger.Logger.fatal("Unable to connect to RabbitMQ", code.ExitCode.RABBIT)

    def _reconnect(self):
        if self._parameters:
            logger.Logger.info("Reconnect to RabbitMQ...")
            self._connection = pika.BlockingConnection(self._parameters)
            logger.Logger.info("Reconnect to RabbitMQ successfully")
        else:
            logger.Logger.fatal("Connection parameters were not specified", code.ExitCode.RABBIT)

    def reconnect(self):
        try:
            self._reconnect()
        except exceptions.AMQPConnectionError:
            logger.Logger.fatal("Unable to reconnect to RabbitMQ", code.ExitCode.RABBIT)

    def _close(self):
        if self._connection:
            if self._connection.is_open:
                self._connection.close()
                logger.Logger.info("Connection with RabbitMQ closed successfully")
        else:
            logger.Logger.warning("The connection is already closed")

    def _get_channel(self):
        if self._connection:
            if self._connection.is_open:
                return self._connection.channel()
            else:
                logger.Logger.warning("Connection closed, attempt to reconnect...")
                self.reconnect()
                return self._connection.channel()
        else:
            logger.Logger.fatal("Connection has not been opened", code.ExitCode.RABBIT)

    def get_channel(self):
        try:
            return self._get_channel()
        except exceptions.AMQPChannelError:
            logger.Logger.fatal("Unable to disconnect from RabbitMQ", code.ExitCode.RABBIT)

    def close(self):
        try:
            self._close()
        except exceptions.AMQPConnectionError:
            logger.Logger.fatal("Unable to disconnect from RabbitMQ", code.ExitCode.RABBIT)


