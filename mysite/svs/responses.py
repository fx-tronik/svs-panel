from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import Camera, Camera_type, Zone
from django.core.serializers import serialize
from .serializers import CameraSerializer
from rest_framework.renderers import JSONRenderer

def cameras(request):
    #print(serialize('json', Camera.objects.all()))
    #for camera in Zone.objects.all():
    #    print(camera)
    #    camera = CameraSerializer(camera)
    #    print(camera.data)

    data = Camera.objects.all()

    data = CameraSerializer(data, many=True).data
    #json = JSONRenderer().render(data)
    #print(json)
    return JsonResponse(data, safe=False)
