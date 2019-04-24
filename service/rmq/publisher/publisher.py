import pika
import pika.channel
import service.rmq.connection.connection as rmq
import util.logger.logger as logger


class RMQPublisher:
    def __init__(self, connection, exchange):
        self._connection: rmq.RMQConnection = connection
        self._channel: pika.channel.Channel = self._connection.get_channel()
        self._exchange = exchange

    def _publish(self, routing_key, body, properties, mandatory):
        self._channel.basic_publish(self._exchange, routing_key, body, properties, mandatory)

    def publish(self, routing_key, body, properties=None, mandatory=False):
        try:
            self._publish(routing_key, body, properties, mandatory)
        except:
            pass