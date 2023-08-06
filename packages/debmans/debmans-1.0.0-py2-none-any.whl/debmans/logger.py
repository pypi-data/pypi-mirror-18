import logging
import logging.handlers
import warnings

from debmans.utils import find_parent_module

# not sure why logging._levelNames are not exposed...
levels = ['CRITICAL',
          'ERROR',
          'WARNING',
          'INFO',
          'DEBUG']


def _log_warning(message, category, filename, lineno, file=None, line=None):
    # for warnings, we just want to use the logging system, not stderr or other files
    msg = "{0}:{1}: {2}: {3}".format(filename, lineno, category.__name__, message)
    logger = logging.getLogger(find_parent_module())
    # Note: the warning will look like coming from here,
    # but msg contains info about where it really comes from
    logger.warning(msg)


def setup_logging(name='debmans', level='info', syslog=False, stream=None):
    """setup logging module according to the arguments provided"""
    logger = logging.getLogger('')
    logger.setLevel('DEBUG')
    if syslog:
        sl = logging.handlers.SysLogHandler(address='/dev/log')
        sl.setFormatter(logging.Formatter(name+'[%(process)d]: %(message)s'))
        # convert syslog argument to a numeric value
        sl.setLevel(syslog.upper())
        logger.addHandler(sl)
        logger.debug('configured syslog level %s' % syslog)
    handler = logging.StreamHandler(stream)
    handler.setFormatter(logging.Formatter('%(message)s'))
    handler.setLevel(level.upper())
    logger.addHandler(handler)
    warnings.showwarning = _log_warning
