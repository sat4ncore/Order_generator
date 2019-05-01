from config.constant.module import RabbitMQModule
from config.constant.exit_code import RABBIT
from util.reporter.reporter import Reporter
from util.collector.collector import OrderCollector
import pika.exceptions
import pika.channel
import logging
import threading

LOGGER = logging.getLogger(RabbitMQModule.CONSUMER)


class RMQConsumer(threading.Thread):
    def __init__(self, parameters):
        super(RMQConsumer, self).__init__()
        self._parameters = parameters
        self._connection = None
        self._channel = None
        self._queues = []
        self._stop_event = False

    @OrderCollector.collect
    @Reporter.update_statistics
    def _consume_callback(self, channel, method_frame, header_frame, body):
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        return body

    def _consume(self, queue, exclusive, consumer_tag):
        if not self._connection:
            self._connect()
        if queue not in self._queues:
            self._queues.append(queue)
        self._channel.basic_consume(queue, self._consume_callback, exclusive, consumer_tag)

    def consume(self, queue, exclusive=False, consumer_tag=None):
        try:
            self._consume(queue, exclusive, consumer_tag)
        except pika.exceptions.AMQPChannelError as ex:
            LOGGER.error(ex)

    def _connect(self):
        try:
            self._connection = pika.BlockingConnection(self._parameters)
            self._channel = self._connection.channel()
            self._channel.basic_qos(prefetch_count=1)
            LOGGER.info("Connection to RabbitMQ successfully established")
        except pika.exceptions.AMQPConnectionError:
            LOGGER.fatal("Incorrect connection parameters or time out")
            exit(RABBIT)

    def _start_consuming(self):
        if self._connection:
            LOGGER.info("Start of the consumer...")
            self._channel.start_consuming()
        else:
            LOGGER.warning("Set queues for consuming")

    def run(self):
        while not self._stop_event:
            try:
                self._start_consuming()
            except pika.exceptions.AMQPConnectionError:
                if not self._stop_event:
                    LOGGER.info("Reconnect to RabbitMQ...")
                    self._connect()
                    for queue in self._queues:
                        self.consume(queue)
                    continue
        try:
            self._connection.close()
            LOGGER.info("Connection to RabbitMQ closed")
        except pika.exceptions.ConnectionWrongStateError as ex:
            LOGGER.error(ex)

    def stop(self):
        try:
            self._stop_event = True
            self._channel.stop_consuming()
            LOGGER.info("Consuming stopped")
        except (pika.exceptions.StreamLostError, AssertionError):
            pass
