import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PathfinderApi.settings')

app = Celery('pathfinder_project')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_url = os.environ.get("CELERY_BROKER_URL")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


# pathfinder_project/__init__.py
from .celery import app as celery_app

__all__ = ('celery_app',)