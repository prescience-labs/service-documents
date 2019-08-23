from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config',
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

app.conf.update(result_expires=3600)
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

if __name__ == '__main__':
    app.start()


@app.task
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
