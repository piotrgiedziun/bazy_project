from django.conf.urls import patterns, url
from django.contrib.auth.views import login as auth_login, password_reset,\
    password_reset_done, password_reset_confirm, password_reset_complete,\
    password_change_done, password_change

import views

urlpatterns = patterns('bazy.views',
    url(r'^$', views.home, name='home'),

    # panels
    url(r'^panel/main$', views.panel_komunikaty,  name='panel'),
    url(r'^panel/rozliczenia$', views.panel_rozliczenia,  name='panel_rozliczenia'),
    url(r'^panel/komunikaty$', views.panel_komunikaty,  name='panel_komunikaty'),
    url(r'^panel/komunikat/(?P<news_pk>\d+)$', views.panel_komunikat,  name='panel_komunikat'),
    url(r'^panel/oplaty/main$', views.panel_oplaty, name='panel_oplaty'),
    url(r'^panel/oplaty/chart/1$', views.panel_oplaty_chart_1, name='panel_oplaty_chart_1'),
    url(r'^panel/oplaty/chart/2$', views.panel_oplaty_chart_2, name='panel_oplaty_chart_2'),
    url(r'^panel/export$', views.panel_export_main,  name='panel_export_main'),
    url(r'^panel/export/(?P<year>\d+)$', views.panel_export,  name='panel_export'),

    # auth
    url(r'^auth/logout$', views.logout, name='logout'),
    url(r'^auth/login/$', auth_login, {'template_name': 'auth/login.html', 'extra_context': {'title': 'Zaloguj'}}, name='login'),

    # pass change
    url(r'^panel/password/change/$', password_change, 
        {'template_name': 'auth/password_change.html', 'post_change_redirect': '/panel/password/change/done/'}, name='password_change'),
    url(r'^panel/password/change/done/$', views.password_change_done,  name='password_change_done'),
    # pass reset
    url(r'^auth/password/reset/$', password_reset,
        {'template_name': 'auth/password_reset.html', 'email_template_name': 'auth/password_reset_email.html'}, name='password_reset'),
    url(r'^auth/password/reset/done/$', password_reset_done),
    url(r'^auth/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm,
        {'post_reset_redirect' : '/auth/password/done/'}),
    url(r'^auth/password/done/$', password_reset_complete,
        {'template_name': 'auth/password_reset_complete.html'}),
)