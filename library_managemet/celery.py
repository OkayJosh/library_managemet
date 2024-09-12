"""
Celery configuration.
"""
import os
from celery import Celery

from django.conf import settings

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'llm.settings')


app = Celery('library_managemet', broker=settings.CELERY_BROKER_URL)


# Load the celery settings from the Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.broker_connection_retry_on_startup = True