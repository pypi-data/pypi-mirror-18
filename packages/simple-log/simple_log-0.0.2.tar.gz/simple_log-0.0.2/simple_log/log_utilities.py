"""
Wrapper around the standard logging module to provide a simplified interface with sensible defaults

Written in and tested against Python 3 only.

Licensed under the MIT license - https://opensource.org/licenses/MIT
"""
__version__ = (0, 0, 2)
__date__ = (2016, 11, 11)
__author__ = "Andrew J Todd esq. <andy47@halfcooked.com>"

import logging

MESSAGE_FORMAT = '%(asctime)s %(levelname)s:: %(message)s'
DATE_FORMAT = '%Y.%m.%d %T'

logs = {}


def get_log(logname=None):
    """Return a log object called `<logname>`

    If you don't specify a `<logname>` your returned object will have the name `default`

    Log objects returned by this function have a logging level of `'INFO'` and a
    sensible message output format including the current date and time and then the
    log level followed by the log message.
    """
    if not logname:
        log_name = 'default'
    else:
        log_name = logname
    if log_name in logs:
        return logs[log_name]
    else:
        logger = logging.getLogger(log_name)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(MESSAGE_FORMAT, DATE_FORMAT)
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        logs[log_name] = logger
        return logger


def add_file(log_name, file_name):
    """Add a file handler to log messages directed to `<log_name>` to `<file_name>`

    We can accept either a log object or the name of a log object in the `<log_name>` parameter
    """
    file_handler = logging.FileHandler(file_name, "a")
    file_formatter = logging.Formatter(MESSAGE_FORMAT, DATE_FORMAT)
    file_handler.setFormatter(file_formatter)
    if type(log_name) is logging.Logger:
        log_name.addHandler(file_handler)
    elif log_name in logs:
        logs[log_name].addHandler(file_handler)
