import os
from dotenv import load_dotenv
from celery import Celery

load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'street_ninja_server.settings')

app = Celery('street_ninja_server')
app.conf.update(
    beat_scheduler="django_celery_beat.schedulers.DatabaseScheduler",
)
# app.conf.beat_scheduler = "django_celery_beat.schedulers.DatabaseScheduler"
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()






@app.task(bind=True)
def debug_task(self):
    ...
    # print(f'Request: {self.request!r}')
