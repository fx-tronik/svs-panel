from django.urls import path
from . import views, responses

urlpatterns = [
    path('test', views.request_page, name='request_page'),
    path('', views.index, name='index'),
    path('cameras', responses.cameras, name='cameras'),
    path('request', views.request_page, name='request'),
    path('zoneconfig', views.zone_config, name='Zones')
]
