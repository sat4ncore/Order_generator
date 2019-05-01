from config.constant.exit_code import RABBIT
from config.constant.module import RabbitMQModule
import logging
import pika
import pika.exceptions

LOGGER = logging.getLogger(RabbitMQModule.SERVICE)


class RMQService:
    def __init__(self):
        self._parameters = None
        self._connection = None
        self._channel = None

    def _open(self, host, port, virtual_host, user, password, connection_attempts, retry_delay):
        credentials = pika.PlainCredentials(user, password)
        self._parameters = pika.ConnectionParameters(host, port, virtual_host, credentials,
                                                     connection_attempts=connection_attempts,
                                                     retry_delay=retry_delay)
        self._connect()

    def open(self, host="localhost", port=5672, virtual_host="/", user="guest",
             password="guest", connection_attempts=15, retry_delay=1):
        try:
            LOGGER.info("Attempt to connect to RabbitMQ...")
            self._open(host, port, virtual_host, user, password, connection_attempts, retry_delay)
            LOGGER.info("Connection to RabbitMQ successfully established")
        except pika.exceptions.AMQPConnectionError:
            LOGGER.fatal("Incorrect connection parameters or time out")
            exit(RABBIT)

    @property
    def parameters(self):
        if self._parameters:
            return self._parameters
        else:
            return False

    def _close(self):
        self._connection.close()

    def _connect(self):
        self._connection = pika.BlockingConnection(self._parameters)
        self._channel = self._connection.channel()

    def _exchange_declare(self, exchange, exchange_type, passive, durable, auto_delete, internal):
        if not self._connection:
            self._connect()
        self._channel.exchange_declare(exchange, exchange_type, passive, durable, auto_delete, internal)

    def exchange_declare(self, exchange, exchange_type="direct", passive=False, durable=False, auto_delete=False, internal=False):
        try:
            LOGGER.info(f"Exchange point declaration with name {exchange} and type {exchange_type}")
            self._exchange_declare(exchange, exchange_type, passive, durable, auto_delete, internal)
        except pika.exceptions.AMQPChannelError as ex:
            LOGGER.error(ex)

    def close(self):
        try:
            if self._connection:
                LOGGER.info("Closes connection with RabbitMQ...")
                self._close()
                LOGGER.info("Connection successfully closed")
        except pika.exceptions.ConnectionWrongStateError as ex:
            LOGGER.error(ex)

    def _queue_declare(self, queue, passive, durable, exclusive, auto_delete):
        if not self._connection:
            self._connect()
        self._channel.queue_declare(queue, passive, durable, exclusive, auto_delete)

    def queue_declare(self, queue, passive=False, durable=False, exclusive=False, auto_delete=False):
        try:
            LOGGER.debug(f"Queue declaration with name {queue}")
            self._queue_declare(queue, passive, durable, exclusive, auto_delete)
        except pika.exceptions.AMQPChannelError as ex:
            LOGGER.error(ex)

    def _queue_bind(self, queue, exchange, routing_key):
        if not self._connection:
            self._connect()
        self._channel.queue_bind(queue, exchange, routing_key)

    def queue_bind(self, queue, exchange, routing_key=None):
        try:
            self._queue_bind(queue, exchange, routing_key)
        except pika.exceptions.AMQPChannelError as ex:
            LOGGER.error(ex)

def queue_delete():
    from config.constant.order import Status
    params = pika.ConnectionParameters(host="172.17.0.3")
    cnx = pika.BlockingConnection(params)
    ch = cnx.channel()
    for status in Status.ALL:
        ch.queue_delete(status)

if __name__ == "__main__":
    queue_delete()