from celery import Celery

from ct_core_api.api.app import config


celery = Celery(__name__, broker=config.ProductionConfig.CELERY_BROKER_URL)
