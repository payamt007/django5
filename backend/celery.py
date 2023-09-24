import os
from datetime import timedelta

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

BROKER = settings.CACHES["default"]["LOCATION"]
app = Celery("backend", broker=BROKER)

app.config_from_object("django.conf:settings", namespace="CELERY")
# app.conf.beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self) -> None:
    print(f"Request: {self.request!r}")


app.conf.beat_schedule = {
    "scrap_task": {
        "task": "rss_parser.tasks.read_feed_links",
        "schedule": timedelta(
            seconds=settings.FEED_READER["DEFAULT_PARSING_TIME_LOOP"]
        ),
    },
}
