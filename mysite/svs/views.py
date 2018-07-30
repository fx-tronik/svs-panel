from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .tasks import mqtt_send
from django.views.generic.list import ListView
from .models import Camera
import json
# Create your views here.



def video(request):

    return render(request, 'svs/video.html')


class CameraListView(ListView):

    model = Camera
    paginate_by = 100  # if pagination is desired


def index(request):
    data = {'alerts': [] }
    #data['alerts'] = []

    dict = {}
    dict['component-id'] = 'DMX'
    dict['action'] = 'send'
    dict['param'] = '360x250'
    data['alerts'].append(dict)
    data['alerts'].append(dict)
    # {"alerts": [{"component-id": "DMX", "action": "send", "param": "360x250"}]}'
    json_obj = json.dumps(data)
    print(json_obj)
    mqtt_send.delay('ws-arm/alerts', json_obj)
    return HttpResponse("123")


payload = 0


def request_page(request):
    global payload
    if(request.GET.get('mybtn')):
        mqtt_send('request1').delay()
    else:
        mqtt_send.delay('ws-debug', str(payload))
        payload = payload+1
    return render(request, 'svs/index.html')


def zone_config(request):

    return render(request, 'svs/ZoneConfig.html')
