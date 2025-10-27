from django.contrib.auth import authenticate
from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.template import loader
from flask_login import login_required

def login(request):
    # render the login template once we add it
    return render(request, 'home/home.html')

@login_required
def chatroom(request, room_name):
    return render(request, 'chatroom/chatroom.html', context={'room_name': room_name})

@login_required
def choose_chatroom(request):
    template = loader.get_template('chatroom/choose_chatroom.html')
    return HttpResponse(template.render())