from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import Camera, Camera_type, Zone
from django.core.serializers import serialize
from .serializers import CameraSerializer, ZoneSerializer
from rest_framework.renderers import JSONRenderer

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin

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

def camera_urls(request):

    data = Camera.objects.all()

    data = CameraConfigSerializer(data, many=True).data

    return JsonResponse(data, safe=False)

class camera_urls(NestedViewSetMixin, ReadOnlyModelViewSet):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer


class test(NestedViewSetMixin, ModelViewSet):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer


class test1(NestedViewSetMixin, ModelViewSet):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer
