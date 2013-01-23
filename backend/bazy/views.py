# -*- coding: utf-8 -*-
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from models import Newsy

def home(request):
    return render(request, 'home.html', {'title': 'Home'})

@login_required
def panel_oplaty(request):
    return render(request, 'panel/oplaty.html', {'title': 'Oplaty'})

@login_required
def panel_komunikaty(request):
    mieszkaniec = request.user.get_profile()
    newsy = Newsy.objects.filter(mieszkancy=mieszkaniec)

    paginator = Paginator(newsy, 5)

    page = request.GET.get('page')
    try:
        newsy_paginate = paginator.page(page)
    except PageNotAnInteger:
        newsy_paginate = paginator.page(1)
    except EmptyPage:
        newsy_paginate = paginator.page(paginator.num_pages)

    return render(request, 'panel/komunikaty.html', {'title': 'Komunikaty', 'newsy': newsy_paginate, 'pages': paginator.page_range})

@login_required
def panel_komunikat(request, news_pk):
    mieszkaniec = request.user.get_profile()
    news = Newsy.objects.get(mieszkancy=mieszkaniec, pk=news_pk)

    # wyznaczanie nastpnych
    next = Newsy.objects.filter(mieszkancy=mieszkaniec, pk__gt=news_pk)
    if len(next) >= 1:
        next = next[len(next)-1]

    prev = Newsy.objects.filter(mieszkancy=mieszkaniec, pk__lt=news_pk)
    if len(prev) >= 1:
        prev = prev[0]

    return render(request, 'panel/komunikat.html', {'title': 'Komunikaty', 'news': news, 'next':next, 'prev':prev})

@login_required
def password_change_done(request):
    messages.success(request, 'Twoje nowe hasło zostało ustawione.')
    return redirect('panel')

@login_required
def logout(request):
    messages.info(request, 'Zostałeś wylogowany.')
    auth_logout(request)
    return redirect('home')