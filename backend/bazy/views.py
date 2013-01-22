from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html', {'title': 'Home'})

@login_required
def panel_oplaty(request):
    return render(request, 'panel/oplaty.html', {'title': 'Oplaty'})

def panel_komunikaty(request):
    return render(request, 'panel/oplaty.html', {'title': 'Komunikaty'})

@login_required
def logout(request):
    auth_logout(request)
    return redirect(home)