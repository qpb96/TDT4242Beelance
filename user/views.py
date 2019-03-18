from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from projects.models import ProjectCategory
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail


from .forms import SignUpForm, EditProfileForm, UserForm, PostReviewForm

from .models import Review
from projects.models import Project

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
    user = request.user.username
    vieweduser = User.objects.get(username=username)
    reviews = Review.objects.all().filter(reviewed=vieweduser).order_by("-date")
    if user == username:
        return render(request, 'user/myaccount.html', {'reviews': reviews,})
    else:
        user = get_object_or_404(User, username=username)

        return render(request, 'user/userprofile.html', {
            "user_username": user.username,
            "user_first_name": user.first_name,
            "user_last_name": user.last_name,
            "user_email": user.email,
            "user_company": user.profile.company,
            "user_phone": user.profile.phone_number,
            "user_address": user.profile.street_address,
            "user_city": user.profile.city,
            "user_state": user.profile.state,
            "user_postal_code": user.profile.postal_code,
            "user_country": user.profile.country,
            "reviews": reviews,

            "display_full_name": user.profile.display_full_name,
            "display_email": user.profile.display_email,
            "display_phone": user.profile.display_phone,
            "display_company": user.profile.display_company,
            "display_city": user.profile.display_street,
            "display_state": user.profile.display_state,
            "display_postal": user.profile.display_postal,
            "display_street": user.profile.display_street,
            "display_country": user.profile.display_country,

        })




@login_required
def edit_user_profile(request, user_id):
    user = User.objects.get(pk=user_id)

    if request.user == user:
        if request.method == 'POST':
            user_form = UserForm(request.POST, instance=user)
            profile_form = EditProfileForm(request.POST, instance=user.profile)
            if profile_form.is_valid() and user_form.is_valid():
                user_form.save(commit=False)
                profile_form.save(commit=False)
                user.save()

                messages.success(request, ('Your profile was successfully updated!'))
                return redirect('view_user_profile', username=user.username)
            else:
                messages.error(request, ('Please fill out the fields with correct information.'))
        else:
            user_form = UserForm(instance=user)
            profile_form = EditProfileForm(instance=user.profile)
        
        return render(request, 'user/edit_profile.html', {
            'user_form': user_form,
            'profile_form': profile_form
        })



def write_review(request, username, project_id):
    profile = User.objects.get(username=username)
    form = PostReviewForm(request.POST)
    project = Project.objects.get(id=project_id)
    if request.method == 'POST':
        form = PostReviewForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.reviewed = profile
            instance.author = request.user.username
            instance.project = project
            instance.date = timezone.now()
            instance.save()
            messages.success(request, 'Review successfully posted ')
            send_mail(
                str(request.user.username)+ " posted a review " ,
                'A review has been posted on your profile',
                'glanceDJ@gmail.com',
                [str(profile.email)],
                fail_silently=False,
            )
            return redirect('view_user_profile', username=username)
        else:
            form = PostReviewForm()

    return render(request, 'user/write_review.html', {
        'form': form,
        'review_of_user': username,
        'project': project, 
        })

