from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from projects.models import ProjectCategory
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import SignUpForm, ProfileForm, UserForm

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
    # View their own user profile. We just render request.user directly.
    if my_user == username:
        return render(request, 'user/myaccount.html')
    # View others' user profile. Need to get user info from the db.
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

        display_full_name = user.profile.display_full_name
        display_email = user.profile.display_email
        display_phone = user.profile.display_phone
        display_company = user.profile.display_company
        display_city = user.profile.display_street
        display_state = user.profile.display_state
        display_postal = user.profile.display_postal
        display_street = user.profile.display_street
        display_country = user.profile.display_country

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
            "user_country": user_country,
            "display_full_name": display_full_name,
            'display_email': display_email,
            'display_phone': display_phone,
            'display_comapny': display_company,
            'display_city': display_city,
            'display_state': display_state,
            'display_postal': display_postal,
            'display_street': display_street,
            'display_country': display_country,
        })

@login_required
def edit_user_profile(request,user_id):
    my_user = User.objects.get(pk=user_id)

    if request.user == my_user:
        if request.method == 'POST':
            user_form = UserForm(request.POST, instance=my_user)  # The User form is an instance of the User model
            profile_form = ProfileForm(request.POST, instance=my_user.profile) # The Profile form is an instance of the Profile model
            if profile_form.is_valid():
                # Set new user.first_name and last_name
                new_user_info = user_form.save(commit=False)
                my_user.first_name = new_user_info.first_name
                my_user.last_name = new_user_info.last_name

                # Set new user.profile.company, user.profile.phone_number, etc. 
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
            user_form = UserForm(instance=my_user)
            profile_form = ProfileForm(instance=my_user.profile)
        
        return render(request, 'user/edit_profile.html', {
            'user_form': user_form,
            'profile_form': profile_form
        })
    
