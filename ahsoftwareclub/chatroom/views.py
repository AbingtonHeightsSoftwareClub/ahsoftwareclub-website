from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.template import loader

def chatroom(request, room_name):
    return render(request, 'chatroom/chatroom.html', context={'room_name': room_name})

def choose_chatroom(request):
    template = loader.get_template('chatroom/choose_chatroom.html')
    return HttpResponse(template.render())