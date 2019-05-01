from util.serializer.protobuf.serializer import ProtobufSerializer
from config.constant.order import Status
from generator.generator import OrderGenerator
from service.mysql.service import MySQLService
from config.constant.module import MAIN
from service.file.json import JsonFileService
from util.reporter.reporter import Reporter
from generator.builder import OrderBuilder
from service.rmq.service import RMQService
from config.config import ProjectConfig
from service.rmq.consumer import RMQConsumer
from service.rmq.publisher import RMQPublisher
from util.collector.collector import OrderCollector
from config.exchange_config import ExchangeConfig
from service.file.text import TextFileService
import logging.config
import argparse
import logging
import logging.handlers
import subprocess
import time
import threading

LOGGER = logging.getLogger(MAIN)
getchar = None


class Launcher:
    @classmethod
    def launch(cls):
        generator, publisher, consumer_start, consumer_final, collector = cls._initialize()
        cls._execute(generator, publisher, consumer_start, consumer_final, collector)

    @classmethod
    def _initialize(cls):
        arg_parser = argparse.ArgumentParser("Order_generator",
                                             description="The program that generates the change history of orders")
        arg_parser.add_argument("-L", "--log", type=int, dest="log_level", help="1 - DEBUG, 2 - INFO, 3 - WARNING"
                                                                                ", 4 - ERROR, 5 - FATAL")
        arg_parser.add_argument("-V", "--volume", type=int, dest="volume", help="Amount of orders to generate")
        arg_parser.add_argument("-C", "--chunk", type=int, dest="chunk_size", help="Chunk size for batch")
        args = arg_parser.parse_args()

        file_separator = "/" if "/" in subprocess.check_output("pwd", universal_newlines=True) else "\\"

        logging.config.dictConfig(JsonFileService.read(f"config{file_separator}logger.json"))
        if args.log_level:
            LOGGER.setLevel(logging.getLevelName(args.log_level * 10))
        LOGGER.info("Logging successfully configured")
        LOGGER.info("Configure the remaining modules of the program...")

        config = ProjectConfig(**JsonFileService.read("config.json"))
        builder = OrderBuilder(**JsonFileService.read(f"config{file_separator}builder.json"))
        if args.volume:
            config.Generator["volume"] = args.volume
        if args.chunk_size:
            config.Generator["chunk_size"] = args.chunk_size
        generator = OrderGenerator(builder=builder, **config.Generator)
        my_sql = MySQLService()
        my_sql.open(**config.MySQL)
        LOGGER.info("Database schema created")
        exchange_config = ExchangeConfig(**config.Exchange)
        rmq_service = RMQService()
        rmq_service.open(**config.RabbitMQ)
        publisher = RMQPublisher(rmq_service.parameters, exchange_config.exchange)
        consumer_final = RMQConsumer(rmq_service.parameters)
        consumer_start = RMQConsumer(rmq_service.parameters)

        rmq_service.exchange_declare(**config.Exchange, durable=True)
        for status in Status.ALL:
            rmq_service.queue_declare(status, durable=True)
            rmq_service.queue_bind(status, exchange_config.exchange)
            if status in Status.FINALS:
                consumer_final.consume(status)
            else:
                consumer_start.consume(status)

        collector = OrderCollector(my_sql)
        return generator, publisher, consumer_start, consumer_final, collector

    @classmethod
    def _execute(cls, generator, publisher, consumer_start, consumer_final, collector):
        consumer_start.start()
        consumer_final.start()
        collector.start()
        completed = False
        LOGGER.info("Generation and Publishing started...")
        LOGGER.info("Press the enter key to get the report")
        threading.Thread(target=cls._report).start()
        while not completed:
            for order in generator.generate_many():
                if order:
                    LOGGER.debug("Chunk generation and publication...")
                    for record in order:
                        publisher.publish(record.status, ProtobufSerializer.serialize(record))
                else:
                    completed = True
                    LOGGER.info("Generation complete")
                    break
        threading.Thread(target=cls._free, args=(collector, consumer_start, consumer_final)).start()

    @classmethod
    def _report(cls):
        global getchar
        while getchar != "exit":
            getchar = input()
            Reporter.report()
        LOGGER.info("Stop report")

    @classmethod
    def _free(cls, collector, consumer_start, consumer_final):
        while getchar != "exit":
            time.sleep(5)
        LOGGER.info("Free all")
        collector.stop()
        consumer_start.stop()
        consumer_final.stop()

