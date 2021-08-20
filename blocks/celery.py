from __future__ import absolute_import

import os
from celery import Celery
from django.conf import settings

# Ingests block run events
from blocks.event import event_ingestor

# this code copied from manage.py
# set the default Django settings module for the 'celery' app.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blocks.settings")

# you change change the name here
app = Celery("blocks")

# read config from Django settings, the CELERY namespace would make celery
# config keys has `CELERY` prefix
app.config_from_object("django.conf:settings", namespace="CELERY")

# load tasks.py in django apps
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task
def event_ingestor(payload):
    return event_ingestor(payload)
