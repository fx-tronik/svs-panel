from django.urls import path
from . import views

urlpatterns = [
    path('test', views.request_page, name='request_page'),
    path('', views.index, name='index'),
]
