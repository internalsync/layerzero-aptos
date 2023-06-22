# -*- coding: utf-8 -*-
import logging
import colorlog


def load_lines(filename):
    with open(filename) as f:
        return [row.strip() for row in f if row and not row.startswith('#')]


log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')

color_formatter = colorlog.ColoredFormatter(
    '%(log_color)s%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'white,bold',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    },
    reset=True,
    style='%'
)


def setup_color_logging(logger, formatter=color_formatter):
    handler = logging.StreamHandler()
    # handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    # handler.setFormatter(log_formatter)
    logger.addHandler(handler)


def setup_file_logging(logger, log_file, formatter=log_formatter):
    # logging file handler
    file_handler = logging.FileHandler(log_file, mode='a')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
