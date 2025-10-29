from django.urls import path
from . import views

urlpatterns = [
    path("choose_chatroom", views.choose_chatroom, name="choose_chatroom"),
    path("<str:room_name>", views.chatroom, name="chatroom"),
]