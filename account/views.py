from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def account(request):
    return render(
        request,
        'account.html')
