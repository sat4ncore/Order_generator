import pika
import pika.channel
from service.rmq import service as rmq
import pika.exceptions


class RMQPublisher:
    def __init__(self, connection, exchange, exchange_type):
        self._connection: rmq.RMQConnection = connection
        self._channel: pika.channel.Channel = self._connection.get_channel()
        self._exchange = exchange
        self._exchange_type = exchange_type

    def _publish(self, routing_key, body, properties, mandatory):
        self._channel.basic_publish(self._exchange, routing_key, body, properties, mandatory)

    def publish(self, routing_key, body, properties=None, mandatory=False):
        try:
            self._publish(routing_key, body, properties, mandatory)
        except pika.exceptions.StreamLostError:
            self._connection.reconnect()
            self._channel = self._connection.get_channel()
            self._channel.exchange_declare(self._exchange, self._exchange_type)
            self._publish(routing_key, body, properties, mandatory)