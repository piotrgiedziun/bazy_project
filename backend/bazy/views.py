from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404, render

def home(request):
    return render(request, 'home.html', {})

def login(request):
    return render(request, 'login.html', {})