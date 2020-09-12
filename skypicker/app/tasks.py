# Vendor
from datetime import date, timedelta
from celery.schedules import crontab
from celery import shared_task
import requests
# Local
from . import utils
from skypicker.celery import app


@shared_task
def load_flights():
    today = date.today()
    params = {
        'partner': 'picky',
        'fly_from': 'ALA',
        'fly_to': 'CIT',
        'date_from': today.strftime('%d/%m/%Y'),
        'date_to': (today + timedelta(days=30)).strftime('%d/%m/%Y')
    }
    r = requests.get(
        'https://api.skypicker.com/flights',
        params=params
    )
    data = r.json()
    utils.dump_flights(data['data'])


app.conf.beat_schedule = {
    'task-first': {
        'task': 'skypicker.app.tasks.load_flights',
        'schedule': crontab(minute=0, hour=0)
    },
}
