from __future__ import absolute_import

import os
from celery import Celery

# Ingests block run events
from blocks.event import event_ingestor as event_ingestor_run

# this code copied from manage.py
# set the default Django settings module for the 'celery' app.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blocks.settings")

# you change change the name here
app = Celery("blocks")

# read config from Django settings, the CELERY namespace would make celery
# config keys has `CELERY` prefix
app.config_from_object("django.conf:settings", namespace="CELERY")

# load tasks.py in django apps
app.autodiscover_tasks()


@app.task
def event_ingestor(payload):
    return event_ingestor_run(payload)


@app.task
def store_eod_data():
    import data_store.interface

    supported_exchanges = ["US", "KLSE"]
    result = []
    for exchange in supported_exchanges:
        start_date, end_date = data_store.interface.get_date_range_of_missing_data(
            exchange
        )
        response = data_store.interface.store_eod_data(start_date, end_date, exchange)
        result.append(response)

    return all(result)
