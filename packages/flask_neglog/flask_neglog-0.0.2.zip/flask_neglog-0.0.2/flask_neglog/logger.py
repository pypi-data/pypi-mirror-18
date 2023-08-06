import logging.handlers
import os.path

from .utils import ensure_dir


class BetterRotatingFileHandler(logging.handlers.RotatingFileHandler):
    def _open(self):
        ensure_dir(os.path.dirname(self.baseFilename))
        return super(BetterRotatingFileHandler, self)._open()
