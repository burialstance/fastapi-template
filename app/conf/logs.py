import logging
from loguru import logger

from app.conf.settings import settings

DEFAULT_LOG_PATH = settings.LOG_PATH
DEFAULT_LOG_FORMAT = (
    "<level>{level:1.1s}</level> "
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> "
    #"<cyan>{name}:{line:<4d}</cyan> <level>{message}</level>"
    "<level>{message}</level>"
)
DEFAULT_LOG_ROTATION = '2 MB'


class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def configure_log(level=logging.DEBUG, path=DEFAULT_LOG_PATH, write=False):
    logging.basicConfig(handlers=[InterceptHandler()], level=level)
    if write:
        logger.add(path, level=level, format=DEFAULT_LOG_FORMAT, rotation=DEFAULT_LOG_ROTATION)
