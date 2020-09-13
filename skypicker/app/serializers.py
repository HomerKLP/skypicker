# Vendor
from rest_framework import serializers
# Local
from .models import Flight, Airline


class AirlineSerializer(serializers.ModelSerializer):
    """Базовый сериалайзер для авиалиний"""
    class Meta:
        model = Airline
        fields = ['id', 'name']


class FlightSerializer(serializers.ModelSerializer):
    """Базовый сериалайзер для рейсов"""
    class Meta:
        model = Flight
        fields = ['id', 'external_id', 'departure_time', 'arrival_time',
                  'duration', 'city_from', 'city_code_from', 'city_to',
                  'city_code_to', 'price', 'currency', 'booking_token',
                  'airlines']
        read_only_fields = fields

    airlines = AirlineSerializer(many=True)


class CheckFlightSerializer(serializers.Serializer):
    """Сериалайзер для проверки рейса"""
    booking_token = serializers.CharField(required=True)
    bnum = serializers.IntegerField(required=True, min_value=1)
    pnum = serializers.IntegerField(required=True, min_value=1, max_value=9)
    currency = serializers.CharField(required=False)
    adults = serializers.IntegerField(required=False, min_value=1)
    children = serializers.IntegerField(required=False, min_value=1)
    infants = serializers.IntegerField(required=False, min_value=1)
