# Vendor
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.conf import settings
# Local
from .serializers import FlightSerializer, CheckFlightSerializer
from .models import Flight
from .utils import check_flight


class SkyPickerViewset(ListModelMixin, GenericViewSet):
    """Базовый вьюсет для рейсов"""
    serializer_class = FlightSerializer
    queryset = Flight.objects.all().order_by('price')
    filterset_fields = ['city_code_from', 'city_code_to']

    @method_decorator(cache_page(settings.CACHE_TTL))
    def list(self, request, *args, **kwargs):
        return super().list(request)

    def filter_queryset(self, queryset):
        date_from = self.request.query_params.get('date_from')
        if date_from:
            queryset = queryset.filter(departure_time__gte=date_from)

        date_to = self.request.query_params.get('date_to')
        if date_to:
            queryset = queryset.filter(departure_time__lte=date_to)
        return super().filter_queryset(queryset)


class CheckFlightViewset(GenericViewSet):
    serializer_class = CheckFlightSerializer

    def get(self, request, *args, **kwargs):
        """Проверка доступности рейса"""
        params = request.query_params
        serializer = self.get_serializer(data=params)
        serializer.is_valid(raise_exception=True)

        return Response(check_flight(serializer.data))
