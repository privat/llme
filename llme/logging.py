"""Logging setup for the llme logger."""

import logging
import sys

from termcolor import colored

from .errors import AppError

logger = logging.getLogger('llme')


def set_verbose(level):
    "Assign a global verbose level (in number of -v)"
    if level is None:
        level = 0
    # Replace any existing console handler, or the lines would be duplicated
    for h in [h for h in logger.handlers
              if isinstance(h, logging.StreamHandler) and not isinstance(h, logging.FileHandler)]:
        logger.removeHandler(h)
    consolehandler = logging.StreamHandler(sys.stderr)
    consolehandler.setFormatter(ColorFormatter())
    logger.addHandler(consolehandler)
    logging_levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    logging_level = logging_levels[min(level, len(logging_levels) - 1)]
    logger.setLevel(logging_level)
    consolehandler.setLevel(logging_level)
    consolehandler.setFormatter(ColorFormatter())
    logger.info("Log level set to %s", logging.getLevelName(logger.level))

def set_log_file(path):
    """Switch the logger's file handler to write to a new path.
    Removes any existing FileHandler and adds a new one."""
    for h in [h for h in logger.handlers if isinstance(h, logging.FileHandler)]:
        logger.removeHandler(h)
        h.close()
    try:
        filehandler = logging.FileHandler(path)
    except OSError as e:
        raise AppError(f"Can't open log file {path}") from e
    filehandler.setLevel(logging.DEBUG)
    logger.setLevel(logging.DEBUG)
    filehandler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(filehandler)

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
