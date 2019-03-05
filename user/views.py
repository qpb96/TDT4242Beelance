from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from projects.models import ProjectCategory
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import SignUpForm

def index(request):
    return render(request, 'base.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()

            user.profile.company = form.cleaned_data.get('company')

            user.is_active = False
            user.profile.categories.add(*form.cleaned_data['categories'])
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            from django.contrib import messages
            messages.success(request, 'Your account has been created and is awaiting verification.')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'user/signup.html', {'form': form})


@login_required
def get_user_profile(request, username):
    my_user = request.user.username
    if my_user == username:
        print(request.user.username)
        return render(request, 'user/myaccount.html')
    else:
        user = User.objects.get(username=username)
        user_first_name = user.first_name
        user_last_name = user.last_name
        user_email = user.email
        user_username = user.username
#        #user_phone = models.pr
        print(user.username)
        return render(request, 'user/userprofile.html', {
            "user_username": user_username,
            "user_first_name": user_first_name,
            "user_last_name": user_last_name,
            "user_email": user_email,
#            "user_phone": user_phone,
        })