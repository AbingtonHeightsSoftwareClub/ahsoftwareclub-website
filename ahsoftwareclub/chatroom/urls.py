from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login, name="login"),
    path("<str:room_name>", views.chatroom, name="chatroom"),
    path("choose_chatroom", views.choose_chatroom, name="choose_chatroom"),
]