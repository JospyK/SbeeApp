from __future__ 	import absolute_import, unicode_literals
from django.conf 	import settings
from celery 		import Celery
from celery.schedules import crontab
import os

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sbeeapp.settings')

app = Celery('sbeeapp')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)



app.conf.beat_schedule = {
    'send-report-every-single-minute': {
        'task': 'fichiers.tasks.load',
        'schedule': crontab(minute='09', hour='13'),  # change to `crontab(minute=0, hour=0)` if you want it to run daily at midnight
    },
}

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
