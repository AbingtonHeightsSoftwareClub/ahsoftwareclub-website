from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.template import loader

def monopoly(request):
    template = loader.get_template('monopoly.html')
    return HttpResponse(template.render())