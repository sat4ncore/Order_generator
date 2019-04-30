class Status:
    NEW = "new"
    TO_PROVIDER = "to_provider"
    REJECT = "reject"
    FILLED = "filled"
    PARTIAL_FILLED = "partial filled"
    FINALS = (REJECT, FILLED, PARTIAL_FILLED)
    ALL = ((NEW, TO_PROVIDER) + FINALS)


ZONES = ("red", "green", "blue")
DIRECTIONS = ("buy", "sell")
WEEK_TIMESTAMP = 604800000

