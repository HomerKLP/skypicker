# Vendor
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
import requests


class SkyPicker(ModelViewSet):
    def get(self, request, *args, **kwargs):
        response = requests.get(
            'https://api.skypicker.com/flights?fly_from=ALA&fly_to=CIT&date_from=21%2F09%2F2020&date_to=24%2F09%2F2020&partner=picky'
        )
        data = response.json()
        for i in data['data']:
            print(i['price'], i['airlines'])
        return Response()
