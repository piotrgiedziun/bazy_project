# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout
from functools import wraps
from models import Mieszkaniec

def login_mieszkaniec_required(view_func):
    @wraps(view_func)
    def _checklogin(request, *args, **kwargs):
        if not request.user.is_active:
            messages.error(request, "Brak uprawnień")
            return redirect('login')
        try:
        	request.user.get_profile()
        	return view_func(request, *args, **kwargs)
        except Mieszkaniec.DoesNotExist:
            messages.error(request, "To konto nie posiada przypisanego mieszkańca")
            logout(request)
            return redirect('login')
    return _checklogin