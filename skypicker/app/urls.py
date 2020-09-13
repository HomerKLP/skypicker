# Vendor
from django.urls import path
# Local
from . import views


urlpatterns = [
    path(
        'flights/',
        views.SkyPickerViewset.as_view({'get': 'list'}),
        name='flights'
    ),
    path(
        'check-flight/',
        views.CheckFlightViewset.as_view({'get': 'get'}),
        name='check-flight'
    )
]
