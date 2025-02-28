import os
from dotenv import load_dotenv
from celery import Celery
# from django.conf import settings

load_dotenv()

# print("DEBUG: ROUTE_ADMIN is", getattr(settings, "ROUTE_ADMIN", "admin/"))  # 👀 Debug

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'street_ninja_server.settings')

app = Celery('street_ninja_server')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    ...
    # print(f'Request: {self.request!r}')
