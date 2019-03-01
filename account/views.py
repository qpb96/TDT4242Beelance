from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.


def account_home(request, username):
    print(request.user.username)
    return render(request, 'account.html')











