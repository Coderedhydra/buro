from celery import Celery
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "security_testing_framework",
    broker=REDIS_URL,
    backend=REDIS_URL,
)

celery_app.conf.task_routes = {"app.workers.tasks.*": {"queue": "default"}}

@celery_app.task(name="app.workers.tasks.heartbeat")
def heartbeat() -> str:
    return "alive"