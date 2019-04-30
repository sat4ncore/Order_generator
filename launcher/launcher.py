from generator.generator import OrderGenerator
from service.mysql.service import MySQLService
from config.constant.module import MAIN
from service.file.json import JsonFileService
from util.reporter.reporter import Reporter
from generator.builder import OrderBuilder
from config.config import ProjectConfig
import logging.config
import argparse
import logging
import logging.handlers
import subprocess


LOGGER = logging.getLogger(MAIN)


class Launcher:
    @classmethod
    def launch(cls):
        pass
        cls._initialize()
        #cls._execute(generator, publisher, consumer, mysql_service)

    @classmethod
    def _initialize(cls):
        arg_parser = argparse.ArgumentParser("Order_generator",
                                             description="The program that generates the change history of orders")
        arg_parser.add_argument("-L", "--log", type=int, dest="log_level", help="1 - DEBUG, 2 - INFO, 3 - WARNING"
                                                                                ", 4 - ERROR, 5 - FATAL")
        arg_parser.add_argument("-V", "--volume", dest="volume", help="Amount of orders to generate")
        args = arg_parser.parse_args()

        file_separator = "/" if "/" in subprocess.check_output("pwd", universal_newlines=True) else "\\"

        logging.config.dictConfig(JsonFileService.read(f"config{file_separator}logger.json"))
        if args.log_level:
            LOGGER.setLevel(logging.getLevelName(args.log_level * 10))
        LOGGER.info("Logging successfully configured")
        LOGGER.info("Configure the remaining modules of the program...")

        config = ProjectConfig(**JsonFileService.read("config.json"))
        builder = OrderBuilder(**JsonFileService.read(f"config{file_separator}builder.json"))
        generator = OrderGenerator(builder=builder, **config.Generator)
        my_sql = MySQLService()
        my_sql.open(**config.MySQL)
        order = generator.generate()
        my_sql
        """
        config = mapper.ConfigMapper(**file.JsonFileService.read("config.json"))
        logger.Logger(config.Logger)
        logger.Logger.info(f"Configuration loaded from file {'config.json'}")
        logger.Logger.info("Program configuration...")
        generator = gen.OrderGenerator(**config.Generator)
        rmq_connection = rmq.RMQConnection()
        rmq_connection.open(**config.RabbitMQ)
        rmq_service = rmqs.RMQService(rmq_connection)
        rmq_service.exchange_declare(**config.Publisher)
        publisher_config = rmqm.RabbitMQPublisherMapper(**config.Publisher)
        for status in genc.GeneratorConsts.STATUSES:
            rmq_service.queue_declare(status)
            rmq_service.queue_bind(status, publisher_config.exchange)
        publisher = rmqp.RMQPublisher(rmq_connection, **config.Publisher)
        consumer = rmqc.RMQConsumer(rmq_connection)
        mysql_service = mysqls.MySqlService()
        mysql_service.open(**config.MySQL)
        mysql_service.execute(text.TextFileService.read('schema.sql'))
        logger.Logger.info("Program configuration complete")
        return generator, publisher, consumer, mysql_service


    @classmethod
    def _execute(cls, generator, publisher, consumer, mysql_service):
        completed = False
        report = threading.Thread(target=cls._report)
        report.start()
        logger.Logger.info("Run generation and publication to RabbitMQ...")
        while not completed:
            for order_record in generator.generate_many():
                if order_record:
                    for order in order_record:
                        publisher.publish(order.status, serializer.ProtoSerializer.serialize(order))
                else:
                    logger.Logger.info("Generation complete")
                    completed = True
                    break
        logger.Logger.info("You can get a report by pressing the enter key.")
        consumer.start_consuming()
        store.Storage.prepare_queries()
        logger.Logger.info("Insert orders to database...")
        mysql_service.execute(mysqlc.MySQLConstant.INSERT, store.Storage.storage, True)
        logger.Logger.info("Insert succesfull")

    @classmethod
    def _report(cls):
        try:
            while True:
                if input().encode() == b"":
                    reporter.Reporter.report()
        except KeyboardInterrupt:
            logger.Logger.info("Stop reporting")

    @classmethod
    def _free(cls):
        pass
        """
