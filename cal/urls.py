from django.conf.urls import url, include
from django.contrib import admin
from cal import views, models

app_name = 'cal'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^newevent/$', views.newevent, name='newevent'),
    url(r'^events/(\d+)/', views.viewevent, name='viewevent'),
    url(r'^(?P<month>\d+)/(?P<year>\d+)$', views.home, name='another-month'),
    url(r'^delete_event/(?P<id>\d+)$', views.delete_event, name='delete_event'),
]
