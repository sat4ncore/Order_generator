import service.converter.convert as conv


class Storage:
    storage = []

    @classmethod
    def append_storage(cls, func):
        def receive_wrapper(*args):
            cls.storage.append(func(*args))
        return receive_wrapper

    @classmethod
    def pop_storage(cls, func):
        def saved_wrapper(*args):
            res = func(*args)
            cls.storage.pop()
            return res
        return saved_wrapper

    @classmethod
    def prepare_queries(cls):
        cls.storage = [tuple(store) for store in cls.storage]
