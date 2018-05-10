import logging

from kernel_upgrader.values.Constants import LOG_FORMAT_TYPE


def setup_logging(logger_name: str, log_file: str, level=logging.DEBUG):
    new_logging = logging.getLogger(logger_name)
    logging_formatter = logging.Formatter(LOG_FORMAT_TYPE)
    logging_file_handler = logging.FileHandler(log_file, mode="w")
    logging_stream_handler = logging.StreamHandler()

    logging_file_handler.setFormatter(logging_formatter)
    logging_stream_handler.setFormatter(logging_formatter)

    new_logging.setLevel(level)
    new_logging.addHandler(logging_file_handler)
    new_logging.addHandler(logging_stream_handler)
