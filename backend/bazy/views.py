# -*- coding: utf-8 -*-
# django
from django.contrib.auth.models import User, Group
from django.shortcuts import get_list_or_404, render, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.conf import settings

# internal
from models import Newsy, Oplaty, Mieszkaniec
from decorators import login_mieszkaniec_required

# python
from datetime import date
import itertools

# export
from openpyxl import Workbook

def home(request):
    return render(request, 'home.html', {'title': 'Strona główna'})


@login_mieszkaniec_required
def panel_oplaty_chart_1(request):
    return render(request, 'panel/oplaty_chart_1.html', {'title': 'Oplaty (wykres)'})

@login_mieszkaniec_required
def panel_oplaty(request):
    today = date.today()

    # date validation
    try:
        month = int(request.GET.get('month', today.month))
        year = int(request.GET.get('year', today.year))
    except ValueError:
        raise Http404("invalid parms")

    if not month in range(1, 13):
        raise Http404("invalid month")
    if not year in range(2000, today.year+1):
        raise Http404("invalid year")



    mieszkaniec = request.user.get_profile()

    # if does not exists -> 404
    oplaty = get_list_or_404(Oplaty,
        mieszkanie=mieszkaniec.mieszkanie,
        data_platnosci__month=month,
        data_platnosci__year=year,
    )

    pln_sum = sum([oplata.saldo for oplata in oplaty])

    # wyznaczanie nastpnych
    max_date = max([oplata.data_platnosci for oplata in oplaty])
    min_date = min([oplata.data_platnosci for oplata in oplaty])

    next = Oplaty.objects.filter(mieszkanie=mieszkaniec.mieszkanie, data_platnosci__gt=max_date)
    if len(next) >= 1:
        next = next[0]

    prev = Oplaty.objects.filter(mieszkanie=mieszkaniec.mieszkanie, data_platnosci__lt=min_date)
    if len(prev) >= 1:
        prev = prev[len(prev)-1]

    return render(request, 'panel/oplaty.html',
        {'title': 'Oplaty', 'oplaty': oplaty, 'pln_sum': pln_sum, 'next':next, 'prev':prev})

@login_mieszkaniec_required
def panel_komunikaty(request):
    mieszkaniec = request.user.get_profile()
    newsy = Newsy.objects.filter(mieszkancy=mieszkaniec)

    paginator = Paginator(newsy, settings.KOMUNIKATY_PER_PAGE)

    page = request.GET.get('page')
    try:
        newsy_paginate = paginator.page(page)
    except PageNotAnInteger:
        newsy_paginate = paginator.page(1)
    except EmptyPage:
        newsy_paginate = paginator.page(paginator.num_pages)

    return render(request, 'panel/komunikaty.html', {'title': 'Komunikaty', 'newsy': newsy_paginate, 'pages': paginator.page_range})

@login_mieszkaniec_required
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

@login_mieszkaniec_required
def panel_export_main(request):
    mieszkaniec = request.user.get_profile()

    oplaty = Oplaty.objects.filter(
        mieszkanie=mieszkaniec.mieszkanie,
    )
    grouped = itertools.groupby(oplaty, lambda record: record.data_platnosci.strftime("%Y-%m"))
    print grouped
    jobs_by_day = [(day, len(list(jobs_this_day))) for day, jobs_this_day in grouped]
    print jobs_by_day

    return render(request, 'panel/export.html', {'title': 'Eksport'})

@login_mieszkaniec_required
def panel_export(request, type, value):
    wb = Workbook(encoding='utf-8')
    ws = wb.get_active_sheet()
    ws.title = u"Opłaty"

    for i in range(0, 10):
        d = ws.cell(row = i, column = 2)
        d.value = i


    wb.save('export.xlsx')

@login_mieszkaniec_required
def password_change_done(request):
    messages.success(request, 'Twoje nowe hasło zostało ustawione.')
    return redirect('panel')

@login_required
def logout(request):
    messages.info(request, 'Zostałeś wylogowany.')
    auth_logout(request)
    return redirect('home')