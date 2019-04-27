class OrderConstant:
    STATUS_NEW = "new"
    STATUS_TO_PROVIDER = "to_provider"
    STATUS_REJECT = "reject"
    STATUS_FILLED = "filled"
    STATUS_PARTIAL_FILLED = "partial filled"
    FINAL_STATUSES = (STATUS_REJECT, STATUS_FILLED, STATUS_PARTIAL_FILLED)
    STATUSES = ((STATUS_NEW, STATUS_TO_PROVIDER) + FINAL_STATUSES)
    ZONES = ("red", "green", "blue")
    DIRECTIONS = ("buy", "sell")
    WEEK_TIMESTAMP = 604800000
