from django.conf.urls import url, include
from django.contrib import admin
from accounts import views, models

app_name = 'accounts'
urlpatterns = [
    url(r'^new-account/$', views.NewUser, name='newaccount'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
]
