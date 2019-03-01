from django.conf.urls import url
from django.urls import path
from . import views
from account import views
from django.contrib.auth.models import User


urlpatterns = [
    path('<username>', views.account_home, name='account_home'),
#    url(r'^/(?P<username>\w+)/$', views.account, name='account'),
#    url(r'^/(?P<username>\w+)/$', 'account_home', name='account_home'),
]
