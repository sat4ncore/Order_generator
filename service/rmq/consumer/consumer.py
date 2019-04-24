import pika
import pika.channel
import config.constant.generator.const as genc


class RMQConsumer:
    def __init__(self, connection=None):
        self._connection = pika.SelectConnection(on_open_callback=self._on_open)
        self._channel: pika.channel.Channel = self._connection.channel()

    def _callback(self, channel, method, properties, body):
        print(body)
        channel.basic_ack(delivery_tag=method.delivery_tag)


    def _on_open(self, connection):
        connection.channel(self._on_channel_open)

    def _on_channel_open(self, channel):
        for status in genc.GeneratorConsts.STATUSES:
            channel.basic_consume(status, self._callback)

    def start_consume(self):
        try:
            self._connection.ioloop.start()
        except KeyboardInterrupt:
            self._connection.close()