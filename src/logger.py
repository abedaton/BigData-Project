
import logging

class handler(logging.StreamHandler):
    colors = {
        logging.DEBUG: '\033[37m',
        logging.INFO: "\033[92m",
        logging.WARNING: "\033[93m",
        logging.ERROR: "\033[91m",
        logging.CRITICAL: "\033[91m"
    }
    reset = '\033[0m'
    fmtr = logging.Formatter('%(levelname)s %(message)s')

    def format(self, record):
        color = self.colors[record.levelno]
        log = self.fmtr.format(record)
        reset = self.reset
        return color + log + reset