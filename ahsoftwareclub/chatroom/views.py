import time

from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.models import Group

# Create your views here.

from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from sqlalchemy.sql.functions import user


def chatroom(request, room_name):
    user = request.user
    all_groups_list = []
    # for checking if they're in any groups or not
    for group in Group.objects.all():
        all_groups_list.append(group.name)
    # If they're in a room, remove them from it
    if user.groups.filter(name__in=all_groups_list).exists():
        for group in user.groups.all():
            group.user_set.remove(user)
    room = Group.objects.get(name=room_name)
    # add the user to the room
    room.user_set.add(user)
    return render(request, 'chatroom/chatroom.html', context={'room_name': room_name, 'active_users' : room.user_set.all()})

# Configure CSRF when we add room passwords to make things secure.
@csrf_exempt
def choose_chatroom(request):
    if request.method == "POST":
        room_name = request.POST.get('room-name')
        room_group, created = Group.objects.get_or_create(name=room_name)
        return redirect(chatroom, room_name)

    groups = Group.objects.all()
    groups_list = []
    for group in groups:
        # if nobody's in a group, delete the group
        if len(group.user_set.all()) == 0:
            group.delete()
        # otherwise add it to the list of groups
        else:
            groups_list.append(group.name)
    return render(request, 'chatroom/choose_chatroom.html', context={'rooms': groups_list, 'user': request.user})
