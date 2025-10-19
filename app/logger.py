import logging
import sys
from .config import settings

def get_logger(name: str) -> logging.Logger:
    """
    Return a logger with the given name and configured for the application.

    If a logger with the given name already exists and has handlers,
    it is returned immediately to avoid duplicate handlers in tests/CLI reloads.

    The logger's level is set to the value of the LOG_LEVEL setting, defaulting to INFO if not set.

    The logger is configured to output to sys.stdout with a formatter that includes the
    timestamp, log level, logger name, and log message.

    The logger's propagate flag is set to False to prevent log messages from being passed to
    parent loggers.

    :param name: The name of the logger to create.
    :return: A logger with the given name and configured for the application.
    """
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger  # avoid duplicate handlers in tests/CLI reloads

    level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z",
    )
    handler.setFormatter(fmt)
    logger.addHandler(handler)
    logger.propagate = False
    return logger
