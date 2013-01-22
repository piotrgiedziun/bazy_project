from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('bazy.views',
    url(r'^$', views.home, name='home'),
    url(r'^login$', views.login, name='login'),
)