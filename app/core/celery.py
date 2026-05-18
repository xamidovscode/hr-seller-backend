from celery import Celery
from celery.schedules import crontab

from app.core.settings import settings

celery_app = Celery(
    "hr_seller",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.jobs"],
)


BEAT_SCHEDULES = {
    "health": {
        "task": "app.jobs.health",
        "schedule": 5.0,
    },
    "db-backup-hourly": {
        "task": "app.jobs.send_db_backup",
        "schedule": crontab(minute=0),
    },
}

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Tashkent",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    beat_schedule=BEAT_SCHEDULES,
)
