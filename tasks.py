from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task(bind=True)
def example(self):
    logger.info('Example task executed')
    return 'Task completed successfully'

@shared_task(bind=True)
def process_order(self, order_id):
    logger.info(f'Processing order {order_id}')
    # Add your order processing logic here
    return f'Order {order_id} processed'