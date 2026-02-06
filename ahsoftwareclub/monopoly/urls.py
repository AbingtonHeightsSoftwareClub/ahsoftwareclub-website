from django.urls import path
from . import views

urlpatterns = [
    path("choose_game", views.choose_game, name="choose_game"),
    path("<str:room_name>", views.monopoly, name="monopoly")
]