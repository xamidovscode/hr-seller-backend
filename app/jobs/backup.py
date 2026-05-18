import logging
import os
import subprocess
import sys

from app.core.celery import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, name="app.jobs.send_db_backup")
def send_db_backup(self) -> dict:
    try:
        env = os.environ.copy()
        env.setdefault("PYTHONPATH", os.getcwd())
        proc = subprocess.run(
            [sys.executable, "scripts/backup.py"],
            capture_output=True,
            text=True,
            env=env,
        )
        if proc.returncode != 0:
            raise RuntimeError(proc.stderr)
        logger.info(proc.stdout.strip())
        return {"status": "ok"}
    except Exception as exc:
        logger.error(f"Backup xatosi: {exc}", exc_info=True)
        raise self.retry(exc=exc, countdown=60, max_retries=3)