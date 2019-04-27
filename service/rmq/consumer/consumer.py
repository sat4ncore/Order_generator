import pika.exceptions
import pika.channel
import util.serializer.protobuf.serializer as deserializer
import service.rmq.connection.connection as rmq
import util.logger.logger as logger
import config.constant.builder as genc
import util.reporter.reporter as reporter
import util.storage.storage as storage


class RMQConsumer:
    def __init__(self, connection):
        self._connection: rmq.RMQConnection = connection
        self._channel: pika.channel.Channel = self._connection.get_channel()
        self._channel.basic_qos(prefetch_count=1)

    def _callback(self, channel, method, properties, body):
        pass

    @reporter.Reporter.increment_received
    @storage.Storage.append_storage
    def _deserialize(self, body):
        order = deserializer.ProtoSerializer.deserialize(body)
        return order

    def _start_consuming(self):
        while True:
            for status in genc.GeneratorConsts.STATUSES:
                message, properties, body = self._channel.basic_get(status, self._callback)
                if body:
                    self._deserialize(body)

    def start_consuming(self):
        try:
            logger.Logger.info("Start of the consumer... ")
            logger.Logger.info("To stop consuming safely, press Ctrl + C")
            self._start_consuming()
        except KeyboardInterrupt:
            logger.Logger.info("Consuming stopped by keyboard interrupt")
            return
        except (pika.exceptions.ConnectionClosedByBroker, pika.exceptions.ConnectionWrongStateError):
            self._connection.reconnect()
            self._channel = self._connection.get_channel()
            self._channel.basic_qos(prefetch_count=1)
            self._start_consuming()
