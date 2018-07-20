from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .tasks import mqtt_send

# Create your views here.
def index(request):

    return HttpResponse("123")

payload=0

def request_page(request):
    global payload
    if(request.GET.get('mybtn')):
        mqtt_send('request1').delay()
    else:
        mqtt_send.delay('ws-debug',str(payload))
        payload= payload+1
    return render(request,'svs/index.html')

def zone_config(request):

    return render(request, 'svs/ZoneConfig.html')
