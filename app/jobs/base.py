import logging

from app.core.celery import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, name="app.jobs.health")
def health(self) -> None:
    logger.info("WORKING HEALTHY")

