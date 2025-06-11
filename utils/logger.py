import logging, sys

def get_logger(name:str="IoTARP"):
    logger = logging.getLogger(name)
    if logger.handlers: return logger
    h = logging.StreamHandler(sys.stdout)
    h.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                                     "%H:%M:%S"))
    logger.addHandler(h)
    logger.setLevel(logging.INFO)
    return logger
