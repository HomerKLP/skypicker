# Vendor
from django.db.transaction import atomic
# Local
from .models import Flight, Airline


def get_airlines(airlines: list) -> list:
    """Получить массив ID авиалиний"""
    airline_ids = []
    for airline in airlines:
        airline_instance = Airline.objects.get_or_create(
            name=airline
        )
        airline_ids.append(airline_instance[0].id)
    return airline_ids


def create_flight(payload):
    """Создать рейс"""
    with atomic():
        airlines = payload.pop('airlines')
        flight_instance = Flight.objects.create(**payload)
        airline_ids = get_airlines(airlines)
        flight_instance.airlines.set(airline_ids)


def update_flight(instance, payload):
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
