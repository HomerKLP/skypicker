# Vendor
from celery.schedules import crontab
from celery import shared_task
from datetime import date, timedelta
from celery.signals import celeryd_init
import requests
# Local
from . import utils
from skypicker.celery import app


@app.task
def load_flight(fly_from: str, fly_to: str):
    """Загрузить определенный маршрут"""
    today = date.today()
    params = {
        'partner': 'picky',
        'fly_from': fly_from,
        'fly_to': fly_to,
        'date_from': today.strftime('%d/%m/%Y'),
        'date_to': (today + timedelta(days=30)).strftime('%d/%m/%Y')
    }
    r = requests.get(
        'https://api.skypicker.com/flights',
        params=params
    )
    data = r.json()
    utils.dump_flights(data['data'])


@shared_task
def load_flights():
    """Загрузить маршруты"""
    flights = [
        ('ALA', 'TSE'),
        ('TSE', 'ALA'),
        ('ALA', 'MOW'),
        ('MOW', 'ALA'),
        ('ALA', 'CIT'),
        ('CIT', 'ALA'),
        ('TSE', 'MOW'),
        ('MOW', 'TSE'),
        ('TSE', 'LED'),
        ('LED', 'TSE'),
    ]
    for flight in flights:
        load_flight.delay(flight[0], flight[1])


@celeryd_init.connect
def configure_workers(sender=None, conf=None, **kwargs):
    load_flights.delay()


app.conf.beat_schedule = {
    'task-first': {
        'task': 'skypicker.app.tasks.load_flights',
        'schedule': crontab(minute=0, hour=0)
    },
}
