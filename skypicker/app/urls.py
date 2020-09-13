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
]
