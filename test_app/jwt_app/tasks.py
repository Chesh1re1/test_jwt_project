from celery import shared_task
import logging

logger = logging.getLogger('celery')

@shared_task
def test_task():
    x = 2
    y = 3
    result = x + y
    logger.info(f"Task executed: {x} + {y} = {result}")
    return result