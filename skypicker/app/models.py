# Vendor
from django.db import models


class Flight(models.Model):
    class Meta:
        verbose_name = 'Рейс'
        verbose_name_plural = 'Рейсы'

    external_id = models.CharField(
        "ID внешнего сервиса",
        max_length=500,
        db_index=True,
        unique=True
    )
    departure_time = models.PositiveBigIntegerField(
        'Время вылета',
        db_index=True,
    )
    arrival_time = models.PositiveBigIntegerField(
        'Время прибытия',
        db_index=True,
    )
    duration = models.PositiveIntegerField(
        'Время в полете',
    )
    city_from = models.CharField(
        'Город вылета',
        max_length=1000,
    )
    city_code_from = models.CharField(
        'Город вылета (кодовое обозначение)',
        max_length=20,
        db_index=True,
    )
    city_to = models.CharField(
        'Город прибытия',
        max_length=1000,
    )
    city_code_to = models.CharField(
        'Город прибытия (кодовое обозначение)',
        max_length=20,
        db_index=True,
    )
    price = models.PositiveIntegerField(
        'Цена',
        db_index=True
    )
    currency = models.CharField(
        'Валюта',
        default='EUR',
        max_length=10,
    )
    airlines = models.ManyToManyField(
        'app.Airline',
        verbose_name='Авиалинии',
        related_name='flights',
    )
    booking_token = models.CharField(
        'Токен для бронирования',
        max_length=2000,
    )


class Airline(models.Model):
    class Meta:
        verbose_name = 'Авиалиния'
        verbose_name_plural = 'Авиалинии'

    name = models.CharField(
        'Наименование',
        max_length=500,
        db_index=True
    )
