from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .tasks import Test, Test1




# Create your views here.
def index(request):

    return HttpResponse("123")

def request_page(request):
    if(request.GET.get('mybtn')):
        print('test')
    else:
        print('kapusta')

    return render(request,'svs/index.html')
