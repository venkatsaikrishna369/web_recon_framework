# utils/logger.py
import logging
import sys
import config

_logger = None

def setup_logger():
    global _logger
    if _logger:
        return _logger
    logger = logging.getLogger("recon")
    logger.setLevel(getattr(logging, config.LOG_LEVEL.upper(), logging.INFO))
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    _logger = logger
    return logger

def get_logger():
    if _logger is None:
        return setup_logger()
    return _logger