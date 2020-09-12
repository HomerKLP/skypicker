# Vendor
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response



class SkyPicker(ModelViewSet):
    def get(self, request, *args, **kwargs):

        return Response()
