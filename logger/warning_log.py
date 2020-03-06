import logging

logger = logging.getLogger(__name__)
custom_logger = logging.FileHandler('warning.log')
logger.setLevel(logging.WARNING)

format_custom_logger = logging.Formatter("%(message)s")
custom_logger.setFormatter(format_custom_logger)
logger.addHandler(custom_logger)


def warning_log(message):
    """Warning logging

    :param message: message of warning
    """
    logger.warning('{0}'.format(message))
