from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from projects.models import ProjectCategory
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import SignUpForm, ProfileForm

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
def view_user_profile(request, username):
    my_user = request.user.username
    # View their own user profile
    if my_user == username:
        return render(request, 'user/myaccount.html')
    # View others' user profile
    else:
        user = User.objects.get(username=username)
        user_first_name = user.first_name
        user_last_name = user.last_name
        user_email = user.email
        user_username = user.username
        user_company = user.profile.company
        user_phone = user.profile.phone_number
        user_address = user.profile.street_address
        user_city = user.profile.city
        user_state = user.profile.state
        user_postal_code = user.profile.postal_code
        user_country = user.profile.country

        return render(request, 'user/userprofile.html', {
            "user_username": user_username,
            "user_first_name": user_first_name,
            "user_last_name": user_last_name,
            "user_email": user_email,
            "user_company": user_company,
            "user_phone": user_phone,
            "user_address": user_address,
            "user_city": user_city,
            "user_state": user_state,
            "user_postal_code": user_postal_code,
            "user_country": user_country
        })

# Edit user profile only works on the fields that belong to the Profile model,
# not the fields that belong to django's User model like first_name, email, etc.
@login_required
def edit_user_profile(request,user_id):
    my_user = User.objects.get(pk=user_id)

    if request.user == my_user:
        if request.method == 'POST':
            profile_form = ProfileForm(request.POST, instance=my_user.profile)  
            if profile_form.is_valid():
                new_profile = profile_form.save(commit=False)
                my_user.profile = new_profile
                my_user.save()
                from django.contrib import messages
                messages.success(request, ('Your profile was successfully updated!'))
                return redirect('view_user_profile', username=my_user.username)
            else:
                from django.contrib import messages
                messages.error(request, ('Please fill out the fields with correct information.'))
        else:
            profile_form = ProfileForm(instance=my_user.profile)
        
        return render(request, 'user/edit_profile.html', {
            'profile_form': profile_form
        })
    
