from django.shortcuts import render
from django.contrib.auth import get_user_model


# Create your views here.

def home(request):
    User = get_user_model()
    users = User.objects.all()
    return render(request, "home/home.html")