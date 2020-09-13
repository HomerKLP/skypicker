# Vendor
from django.db.transaction import atomic
from django.conf import settings
from rest_framework.exceptions import APIException
import logging
# Local
from .models import Flight, Airline
from .requests import perform_request

logger = logging.getLogger(__name__)


def get_airlines(airlines: list) -> list:
    """Получить массив ID авиалиний"""
    airline_ids = []
    for airline in airlines:
        airline_instance = Airline.objects.get_or_create(
            name=airline
        )
        airline_ids.append(airline_instance[0].id)
    return airline_ids


def create_flight(payload: dict):
    """Создать рейс"""
    with atomic():
        airlines = payload.pop('airlines')
        flight_instance = Flight.objects.create(**payload)
        airline_ids = get_airlines(airlines)
        flight_instance.airlines.set(airline_ids)


def update_flight(instance, payload: dict):
    """Обновить данные рейса"""
    with atomic():
        airlines = payload.pop('airlines')
        for key, value in payload.items():
            setattr(instance, key, value)
        instance.save()
        airline_ids = get_airlines(airlines)
        instance.airlines.set(airline_ids)


def dump_flights(data: dict):
    """Парсим данные и записываем в модель Flight"""
    for i in data:
        try:
            payload = {
                'external_id': i['id'],
                'departure_time': i['dTimeUTC'],
                'arrival_time': i['aTimeUTC'],
                'duration': i['duration']['total'],
                'city_from': i['cityFrom'],
                'city_code_from': i['cityCodeFrom'],
                'city_to': i['cityTo'],
                'city_code_to': i['cityCodeTo'],
                'price': i['price'],
                'booking_token': i['booking_token'],
                'airlines': i['airlines']
            }
        except KeyError:
            continue

        # Создаем или обновляем запись Flight
        try:
            flight_created = Flight.objects.get(
                external_id=payload['external_id']
            )
        except Flight.DoesNotExist:
            create_flight(payload)
        else:
            update_flight(flight_created, payload)


def get_kzt_conversion(eur: float) -> float:
    """Получить эквивалент в тенге"""


def _check_flight(data: dict):
    try:
        if data['flights_invalid'] and not data['flights_checked']:
            raise APIException('Рейс не валидный. Обратитесь к администратуру.',
                               code='400;INVALID_FLIGHT')
        if data['price_change']:
            raise APIException('Цена обновилась. Новая цена - ' +
                               data['tickets_price'],
                               code='203;NEW_PRICE')
        total_price = data['total']
    except KeyError as e:
        error_msg = "can't decode response: " + str(e)
        logger.critical(error_msg)
        raise APIException(error_msg, code='500;DECODE_ERROR')
    else:
        return total_price


def get_kzt_price(eur: float) -> dict:
    """Получить дикт с мультивалютным прайсом"""
    return {
        'EUR': eur,
        'KZT': round(settings.EURO_TO_KZT * eur)
    }


def check_flight(data: dict):
    """Проверяем валидность рейса"""
    response_data = perform_request(settings.CHECK_FLIGHT_URL, params=data)
    total = _check_flight(response_data)
    return {'ok': True,
            'detail': 'Бронирование одобрено!',
            'total_price': get_kzt_price(total)}
