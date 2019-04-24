import util.logger.logger as logger


class Reporter:
    __generated_red_zone = 0
    __generated_green_zone = 0
    __generated_blue_zone = 0
    __received_from_rmq = 0
    __saved_to_database = 0

    @classmethod
    def increment_red_zone(cls, func):
        def generation_wrapper(*args):
            cls.__generated_red_zone += 1
            return func(*args)
        return generation_wrapper

    @classmethod
    def increment_green_zone(cls, func):
        def generation_wrapper(*args):
            cls.__generated_green_zone += 1
            return func(*args)
        return generation_wrapper

    @classmethod
    def increment_blue_zone(cls, func):
        def generation_wrapper(*args):
            cls.__generated_blue_zone += 1
            return func(*args)
        return generation_wrapper

    @classmethod
    def increment_received(cls, func):
        def generation_wrapper(self):
            cls.__received_from_rmq += 1
            return func(self)
        return generation_wrapper

    @classmethod
    def increment_saved(cls, func):
        def generation_wrapper(self):
            cls.__saved_to_database += 1
            return func(self)
        return generation_wrapper

    @classmethod
    def report(cls):
        logger.Logger.info(f"""
                        REPORT
            Order generator by sat4ncore
Currently generated orders:
    red zone  --  {cls.__generated_red_zone}
    green zone  --  {cls.__generated_green_zone}
    blue zone  -- {cls.__generated_blue_zone}
RabbitMQ:
    received  --  {cls.__received_from_rmq}
MySQL:
    saved  --  {cls.__saved_to_database}
                                    """)
