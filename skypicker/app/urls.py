# Vendor
from django.urls import path
# Local
from . import views

urlpatterns = [
    path('flights/', views.SkyPicker.as_view({'get': 'get'})),
]