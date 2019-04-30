from config.constant.module import RabbitMQModule
import pika
import pika.channel
import pika.exceptions
import logging

LOGGER = logging.getLogger(RabbitMQModule.PUBLISHER)


class RMQPublisher:
    def __init__(self, channel, exchange, serializer):
        self._channel: pika.channel.Channel = channel
        self._exchange = exchange
        self._serializer = serializer

    def _publish(self, routing_key, body, properties, mandatory):
        self._channel.basic_publish(self._exchange, routing_key,
                                    self._serializer.serialize(body),
                                    properties, mandatory)

    def publish(self, routing_key, body, properties=None, mandatory=False):
        try:
            self._publish(routing_key, body, properties, mandatory)
        except pika.exceptions.StreamLostError as ex:
            LOGGER.error(ex)
