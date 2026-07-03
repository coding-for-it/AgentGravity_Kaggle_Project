import logging
import os
from logging.handlers import RotatingFileHandler


LOG_FOLDER = "logs"

os.makedirs(LOG_FOLDER, exist_ok=True)


def get_logger(name):

    logger = logging.getLogger(name)

    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    log_file = os.path.join(LOG_FOLDER, f"{name}.log")

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,   # 5 MB
        backupCount=5,              # Keep last 5 log files
        encoding="utf-8"
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    logger.propagate = False

    return logger