# Vendor
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
# Local
from .serializers import FlightSerializer
from .models import Flight


class SkyPickerViewset(ListModelMixin, GenericViewSet):
    """Базовый вьюсет для рейсов"""
    serializer_class = FlightSerializer
    queryset = Flight.objects.all().order_by('price')
