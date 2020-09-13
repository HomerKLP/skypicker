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


class Test(GenericViewSet):
    def list(self, request):
        from .tasks import load_flights
        from rest_framework.response import Response
        load_flights.delay()
        return Response()
