Simple Logging
===============================

* version number: 0.0.1
* date: 2016.11.10
* author: Andrew J. Todd esq.

Overview
--------

A python module to allow you to log. It's a wrapper around the standard logging module with sensible defaults and 
as little configuration as possible.

Installation 
------------

To install use pip:

    $ pip install simple_log


Or clone the repo:

    $ hg clone https://bitbucket.org/andy47/simple_log
    $ python setup.py install
    
Usage
-----

We try and stay true to the name and make using this module as simple as possible. For the simplest case just use

    >>> from simple_log import get_log
    >>> my_log = get_log()
    >>> my_log.info("This is an information message")
    2016.11.10 22:21:51 INFO:: This is an information message
    
If you want to have multiple logs just pass a name to `get_log`

    >>> second_log = get_log('two')
    >>> second_log.debug("This is a debug message")

By default the logging level is set to `'INFO'` (the standard module defaults to `'WARN'`). See the
[logging tutorial](https://docs.python.org/3/howto/logging.html#logging-basic-tutorial) for information on logging 
levels. If you would like to change the logging level, for instance to display 'DEBUG' messages use the `set_level`
function

    >>> from simple_log import get_log, set_level
    >>> my_log = get_log('test_log')
    >>> my_log.debug('This is the first debug message')
    ...
    >>> set_level('test_log', 'DEBUG')
    >>> my_log.debug('This is the second debug message')
    2016.11.10 22:34:55 DEBUG:: This is the second debug message

Contributing
------------

If you would like to contribute please add a pull request - https://bitbucket.org/andy47/simple_log/pull-requests/
