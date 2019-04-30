from config.constant.module import RabbitMQModule
import pika
import pika.exceptions
import logging

LOGGER = logging.getLogger(RabbitMQModule.SERVICE)




class RabbitMQService:
    def __init__(self):
        self._parameters = None
        self._connection = None

    def queue_declare(self, queue, passive=False, durable=False, exclusive=False, auto_delete=False):
        pass

r = RabbitMQService()