import threading


class SingletonMeta(type):
    """
    This is a thread-safe implementation of the Singleton class.
    """

    _instance = None

    _lock: threading.Lock = threading.Lock()
    """
    We now have a lock object to synchronize threads during
    first access to singleton.
    """

    def __call__(cls, *args, **kwargs):
        # Now imagine that the program was just launched.
        # No single object has yet been created, so several threads
        # could easily go through the previous condition and reach
        # lock. The fastest flow will put the lock and move inside.
        # sections, while others are waiting for him here.
        with cls._lock:
            # The first thread reaches this condition and goes inside, creating
            # single object. As soon as this thread leaves the section and releases
            # lock, the next thread can set the lock again and
            # go inside. However, now a single instance will already be created and
            # the thread will not be able to go through this condition, which means the new object is not
            # will be created.
            if not cls._instance:
                cls._instance = super().__call__(*args, **kwargs)
        return cls._instance
