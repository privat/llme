"""Logging setup for the llme logger."""

import logging
import sys

from termcolor import colored

logger = logging.getLogger('llme')


def set_verbose(level):
    "Assign a global verbose level (in number of -v)"
    if level is None:
        level = 0
    consolehandler = logging.StreamHandler(sys.stderr)
    consolehandler.setFormatter(ColorFormatter())
    logger.addHandler(consolehandler)
    logging_levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    logging_level = logging_levels[min(level, len(logging_levels) - 1)]
    logger.setLevel(logging_level)
    consolehandler.setLevel(logging_level)
    consolehandler.setFormatter(ColorFormatter())
    logger.info("Log level set to %s", logging.getLevelName(logger.level))

class ColorFormatter(logging.Formatter):
    """A simple colored formatter."""

    COLORS = [
        (logging.DEBUG, 'light_grey'),
        (logging.INFO, 'cyan'),
        (logging.WARNING, 'light_cyan'),
        (logging.ERROR, 'light_red'),
    ]

    def color(self, record):
        for level, color in self.COLORS:
            if record.levelno <= level:
                return color
        return 'white' # default color

    def format(self, record):
        return f"{colored(record.levelname, self.color(record))}: {record.getMessage()}"
