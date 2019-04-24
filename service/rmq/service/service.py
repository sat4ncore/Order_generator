import service.rmq.connection.connection as rmq
import pika.exceptions as exceptions
import util.logger.logger as logger
import pika.channel


class RMQService:
    def __init__(self, connection=rmq.RMQConnection()):
        self._connection: rmq.RMQConnection = connection
        self._channel: pika.channel.Channel = self._connection.get_channel()

    def exchange_declare(self, exchange, exchange_type='direct', passive=False, durable=False, auto_delete=False):
        try:
            self._channel.exchange_declare(exchange, exchange_type, passive, durable, auto_delete)
        except exceptions.AMQPChannelError:
            logger.Logger.error(f"Cannot declare exchange {exchange} with type {exchange_type}")

    def queue_declare(self, queue, passive=False, durable=False, exclusive=False, auto_delete=False):
        try:
            self._channel.queue_declare(queue, passive, durable, exclusive, auto_delete)
        except exceptions.AMQPChannelError:
            logger.Logger.error(f"Cannot declare queue {queue}")

    def queue_bind(self, queue, exchange, routing_key=None):
        self._channel.queue_bind(queue, exchange, routing_key)

    def queue_delete(self, queue, if_unused=False, if_empty=False):
        try:
            self._channel.queue_delete(queue, if_unused, if_empty)
        except exceptions.AMQPChannelError:
            logger.Logger.error(f"Cannot delete queue {queue}")
