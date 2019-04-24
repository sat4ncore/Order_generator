import generator.generator as gen
import service.file.json.service as file
import config.mapper.mapper as mapper
import service.reporter.reporter as reporter
import util.logger.logger as logger
import service.rmq.connection.connection as rmq
import config.mapper.rmq.mapper as rmqm
import service.rmq.service.service as rmqs
import config.constant.generator.const as genc
import service.rmq.publisher.publisher as rmqp
import service.rmq.consumer.consumer as rmqc


class Launcher:
    @classmethod
    def launch(cls):
        generator, publisher, consumer = cls._initialize()
        cls._execute(generator, publisher, consumer)

    @classmethod
    def _initialize(cls):
        config = mapper.ConfigMapper(**file.JsonFileService.read("config.json"))
        logger.Logger(config.Logger)
        logger.Logger.info(f"Configuration loaded from file {'TODO'}")
        logger.Logger.info("Program configuration...")
        generator = gen.OrderGenerator(**config.Generator)
        rmq_connection = rmq.RMQConnection()
        rmq_connection.open(**config.RabbitMQ)
        rmq_service = rmqs.RMQService(rmq_connection)
        rmq_service.exchange_declare(**config.Publisher)
        publisher_config = rmqm.RabbitMQPublisherMapper(**config.Publisher)
        for status in genc.GeneratorConsts.STATUSES:
            rmq_service.queue_delete(status)
            rmq_service.queue_declare(status, durable=True)
            rmq_service.queue_bind(status, publisher_config.exchange)
        publisher = rmqp.RMQPublisher(rmq_connection, publisher_config.exchange)
        publisher.publish(genc.GeneratorConsts.STATUS_REJECT, "test")
        consumer = rmqc.RMQConsumer()
        consumer.start_consume()

        logger.Logger.info("Program configuration complete")
        return generator, publisher, consumer

    @classmethod
    def _execute(cls, generator, publisher, consumer):
        completed = False
        while not completed:
            for order_record in generator.generate_many():
                if order_record:
                    for order in order_record:
                       pass
                else:
                    logger.Logger.info("Generation complete")
                    completed = True
                    break

        

    @classmethod
    def _report(cls):
        pass


    @classmethod
    def _free(cls):
        pass

