from django.urls import path
from . import views

urlpatterns = [
    path("", views.chatroom, name="chatroom"),
    path("choose_chatroom", views.choose_chatroom, name="choose_chatroom"),
]