import logging

from .logger import BetterRotatingFileHandler
from .utils import ensure_file_dir

DEFAULT_LEVEL = 'WARN'
DEFAULT_BACKUP_COUNT = 5
DEFAULT_FILENAME = 'error.log'
DEFAULT_MAX_BYTE = 1024 * 1024 * 64
DEFAULT_FORMATTER = '%(asctime)s - %(levelname)s - %(message)s'
DEFAULT_ENABLE_CONSOLE = False


class Log(object):
    """
    :param level:
        set this logger level, default is WARN, available values:
        CRITICAL, ERROR, WARN, INFO, DEBUG

    :param filename:
        error log filename, can been absolute file path, Flask-Log will create the
        error log parent directory, default is error.log

    :param backup_count:
        error log Rotate backup count, default is 5

    :param max_byte:
        each log file's max byte, default 64M

    :param formatter:
        log formatter, default is '%(asctime)s - %(levelname)s - %(message)s'

    :param enable_console:
        set up a console handler, default False


    """

    def __init__(self, app=None, **kwargs):
        self._options = kwargs
        self._app = None
        if app is not None:
            self.init_app(app, **kwargs)

    def init_app(self, app, **kwargs):
        self._app = app
        level = self.get_parameter('level', DEFAULT_LEVEL)
        level = level.upper()
        backup_count = self.get_parameter('backup_count', DEFAULT_BACKUP_COUNT)
        max_byte = self.get_parameter('max_byte', DEFAULT_MAX_BYTE)
        filename = self.get_parameter('filename', DEFAULT_FILENAME)
        formatter = self.get_parameter('formatter', DEFAULT_FORMATTER)
        enable_console = self.get_parameter('enable_console', DEFAULT_ENABLE_CONSOLE)

        app.logger.setLevel(level)
        ensure_file_dir(filename)

        file_handler = BetterRotatingFileHandler(filename=filename, maxBytes=max_byte, backupCount=backup_count)
        formatter = logging.Formatter(formatter)
        file_handler.setFormatter(formatter)
        app.logger.addHandler(file_handler)
        if enable_console:
            console = logging.StreamHandler()
            console.setLevel(level)
            formatter = logging.Formatter(DEFAULT_FORMATTER)
            console.setFormatter(formatter)
            app.logger.addHandler(console)

    def get_parameter(self, name, default=None):
        tmp = self._options.get(name)
        if tmp is None:
            parameter_name = 'LOG_{0}'.format(name.upper())
            tmp = self._app.config.get(parameter_name, default)
        return tmp
