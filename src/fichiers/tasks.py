from __future__ import absolute_import, unicode_literals
import datetime
from celery.task import periodic_task
from celery.schedules import crontab
from sbeeapp.celery import app

@periodic_task(run_every=crontab(minute='15', hour="00"))
#@app.task
def load():
    # Do something here
    # like accessing remote apis,
    # calculating resource intensive computational data
    # and store in cache
    # or anything you please
    print('This wasn\'t so difficult')