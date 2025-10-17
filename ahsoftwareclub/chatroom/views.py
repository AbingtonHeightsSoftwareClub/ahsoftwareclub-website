from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.template import loader

def chatroom(request):
    template = loader.get_template('chatroom/chatroom.html')
    return HttpResponse(template.render())

def choose_chatroom(request):
    template = loader.get_template('chatroom/choose_chatroom.html')
    return HttpResponse(template.render())