# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout
from functools import wraps

def login_mieszkaniec_required(view_func):
    @wraps(view_func)
    def _checklogin(request, *args, **kwargs):
        if request.user.is_active:
            try:
            	request.user.get_profile()
            	return view_func(request, *args, **kwargs)
            except:
            	pass
        logout(request)
        messages.error(request, "Brak uprawnień lub to konto nie posiada przypisanego mieszkańca")
        return redirect('login')
    return _checklogin