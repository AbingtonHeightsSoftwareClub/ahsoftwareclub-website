from allauth.core.internal.httpkit import redirect
from django.shortcuts import render
from django.contrib.auth.models import Group

# Create your views here.

from django.http import HttpResponse
from django.template import loader


def chatroom(request, room_name):
    return render(request, 'chatroom/chatroom.html', context={'room_name': room_name})


def choose_chatroom(request):
    if request.method == "POST":
        room_name = request.POST['room_name']
        room = Group.objects.create(name=room_name)
        room.user_set.add(request.user)
        return chatroom(request, room_name)
    groups = Group.objects.all()
    groups_list = []
    for group in groups:
        groups_list.append(group.name)
    print(groups_list)
    return render(request, 'chatroom/choose_chatroom.html', context={'rooms': groups_list, 'user': request.user})
