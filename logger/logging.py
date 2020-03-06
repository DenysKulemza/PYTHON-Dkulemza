import logging
from validation.getters import *

logger = logging.getLogger(__name__)
custom_logger = logging.FileHandler('work.log')
logger.setLevel(logging.INFO)

format_custom_logger = logging.Formatter("%(asctime)s %(message)s")
custom_logger.setFormatter(format_custom_logger)
logger.addHandler(custom_logger)


def loggers(request, center_id, change, entity_id):
    """Logging information

    :param request: request of some url data
    :param center_id: id of some center
    :param change: what was changed
    :param entity_id: id of entity type
    """
    logger.info('Method type {0}. Request url {1}. Center id {2}. Entity type {3}. Entity id {4}'.format(request.method, request.url, center_id, change, entity_id))
