from config.constant.module import RabbitMQModule
import pika
import pika.channel
import pika.exceptions
import logging
import time

LOGGER = logging.getLogger(RabbitMQModule.PUBLISHER)


class RMQPublisher:
    def __init__(self, parameters, exchange):
        self._parameters = parameters
        self._exchange = exchange
        self._connection = None
        self._channel = None
        self._connect()

    def _connect(self):
        self._connection = pika.BlockingConnection(self._parameters)
        self._channel = self._connection.channel()
        LOGGER.info("Connection to RabbitMQ successfully established")

    def _publish(self, routing_key, body, properties, mandatory):
        self._channel.basic_publish(self._exchange, routing_key, body, properties, mandatory)

    def publish(self, routing_key, body, properties=pika.BasicProperties(delivery_mode=2), mandatory=False):
        try:
            self._publish(routing_key, body, properties, mandatory)
        except (pika.exceptions.ConnectionWrongStateError, pika.exceptions.StreamLostError,
                pika.exceptions.ChannelWrongStateError, pika.exceptions.ConnectionClosedByBroker):
            LOGGER.error("Connection lost. Reconnect...")
            self._connect()
            self._publish(routing_key, body, properties, mandatory)
