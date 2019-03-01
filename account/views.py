from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.

@login_required
def get_user_profile(request, username):
    my_user = request.user.username
    if my_user == username:
        print(request.user.username)
        return render(request, 'account.html')
    else:
        user = User.objects.get(username=username)
        user_first_name = user.first_name
        user_last_name = user.last_name
        user_email = user.email
        user_username = user.username
        print(user.username)
        return render(request, 'user_profile.html', {
            "user_username": user_username,
            "user_first_name": user_first_name,
            "user_last_name": user_last_name,
            "user_email": user_email,
        })











