from __future__ import absolute_import
import os
from celery import Celery
from celery.signals import celeryd_init


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

app = Celery('mysite')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@celeryd_init.connect()#sender='worker12@example.com')
def testujemy(conf=None, **kwargs):
    from svs.tasks import Test, Test1
    Test.apply_async(task_id='t1')
    Test1.apply_async(task_id='t2')
