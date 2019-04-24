import config.constant.util.color as color
import random


class LoggerConsts:
    DEFAULT_FORMAT = f"{random.choice(color.Colors.COLORS)}{color.Colors.BOLD}%(message)s"
    MAIN_MODULE = "program"
