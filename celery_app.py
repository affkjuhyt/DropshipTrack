from celery import Celery
from celery.signals import after_setup_logger
import logging

app = Celery('dropship-tracker')
app.config_from_object('celeryconfig')

# Configure logging
@after_setup_logger.connect
def setup_loggers(logger, *args, **kwargs):
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler = logging.FileHandler('celery.log')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# Import tasks
app.autodiscover_tasks(['tasks'])

if __name__ == '__main__':
    app.start()