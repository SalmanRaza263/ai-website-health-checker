from celery import Celery
from app.core.config import config
import os

celery_app = Celery(
    "worker",
    broker=config.CELERY_BROKER_URL,
    backend=config.CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=config.MAX_SCAN_TIME,
    task_soft_time_limit=config.MAX_SCAN_TIME - 10,
)

# Auto-discover tasks
celery_app.autodiscover_tasks(["app.workers"])