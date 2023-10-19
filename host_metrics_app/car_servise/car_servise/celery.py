import celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'car_servise.settings')

app = celery.Celery('car_servise')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()




