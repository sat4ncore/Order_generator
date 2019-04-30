from config.constant.module import RabbitMQModule
from config.constant.exit_code import RABBIT
from util.reporter.reporter import Reporter
import pika.exceptions
import pika.channel
import logging
import threading

LOGGER = logging.getLogger(RabbitMQModule.CONSUMER)


class RMQConsumer(threading.Thread):
    def __init__(self, parameters, deserializer):
        super(RMQConsumer, self).__init__()
        self._parameters = parameters
        self._deserializer = deserializer

    def _consume_callback(self, channel, method_frame, header_frame, body):
        print(self.name, body)
        body = self._deserializer.deserialize(body)
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        return body

    def consume(self, queue):

    def _start_consuming(self, *args):
        connection = pika.BlockingConnection(self._parameters)
        channel = connection.channel()
        channel.basic_qos(prefetch_count=1)
        for queue in args:
            LOGGER.debug(f"Basic consume queue {queue}")
            channel.basic_consume( queue, self._consume_callback)
        LOGGER.info("Start of the consumer...")
        channel.start_consuming()

    def _stop_consuming(self):
        pass
        #self._channel.close()

    def stop_consuming(self):
        try:
            self._stop_consuming()
        except pika.exceptions.ChannelClosed as ex:
            LOGGER.error(ex)

    def run(self, *args) -> None:
        self.start_consuming(*args)

    def start_consuming(self, *args):
        try:
            args = ("test",)
            if args:
                self._start_consuming(*args)
                return True
            else:
                LOGGER.warning("No queues for consuming")
                return False
        except pika.exceptions.AMQPConnectionError as ex:
            LOGGER.fatal(ex)
            exit(RABBIT)


from util.serializer.protobuf.serializer import ProtobufSerializer

params = pika.ConnectionParameters("172.17.0.3", retry_delay=1, connection_attempts=15)
cnx = pika.BlockingConnection(params)
ch = cnx.channel()
test= ch.queue_declare("test", durable=True)
ch.queue_bind("test", "amq.direct")
#ch.queue_bind("test", "amq.direct")
d = RMQConsumer(params, ProtobufSerializer)
c = RMQConsumer(params, ProtobufSerializer)
d.start()
c.start()