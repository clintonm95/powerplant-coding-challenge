import logging


def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Create file handler for logging
    file_handler = logging.FileHandler("logs/app.log")
    file_handler.setLevel(logging.ERROR)

    # Create a logging format
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger
