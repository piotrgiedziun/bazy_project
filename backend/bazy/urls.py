from django.conf.urls import patterns, url
from django.contrib.auth.views import login as auth_login
from django.views.generic import RedirectView
import views

urlpatterns = patterns('bazy.views',
    url(r'^$', views.home, name='home'),
    url(r'^logout$', views.logout, name='logout'),

    # panels
    url(r'^panel$', views.panel_komunikaty,  name='panel'),
    url(r'^panel/komunikaty$', views.panel_komunikaty,  name='panel_komunikaty'),
    url(r'^panel/oplaty$', views.panel_oplaty,  name='panel_oplaty'),

    # auth
    url(r'^login/$', auth_login, {'template_name': 'login.html', 'extra_context': {'title': 'Sign In'}}, name='login'),
)