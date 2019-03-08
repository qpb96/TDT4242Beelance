from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from projects.models import ProjectCategory, Profile

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    company = forms.CharField(max_length=30, required=False, help_text= 'Here you can add your company.')
    phone_number = forms.CharField(max_length=50)

    street_address = forms.CharField(max_length=50)
    city = forms.CharField(max_length=50)
    state = forms.CharField(max_length=50)
    postal_code = forms.CharField(max_length=50)
    country = forms.CharField(max_length=50)


    email = forms.EmailField(max_length=254, help_text='Inform a valid email address.')
    email_confirmation = forms.EmailField(max_length=254, help_text='Enter the same email as before, for verification.')
    categories = forms.ModelMultipleChoiceField(queryset=ProjectCategory.objects.all(), help_text='Hold down "Control", or "Command" on a Mac, to select more than one.')


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'categories', 'company' , 'email', 'email_confirmation', 'password1', 'password2', 'phone_number', 'street_address', 'city', 'state', 'postal_code', 'country')


class UserForm(forms.ModelForm):
    # Need to define these fields as CharField to retrieve them as text fields in edit_profile.html
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254, help_text='Inform a valid email address.')

    class Meta: 
        model = User    
        fields = ('first_name', 'last_name', 'email',)

class EditProfileForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(queryset=ProjectCategory.objects.all(), required=False, help_text='Hold down "Control", or "Command" on a Mac, to select more than one.')

    class Meta: 
        model = Profile
        fields = (
            'display_full_name',
            'display_email',
            'categories',
            'phone_number',             'display_phone',
            'company' ,                 'display_company',
            'street_address',           'display_street',
            'city',                     'display_city',
            'state',                    'display_state',
            'postal_code',              'display_postal',
            'country',                  'display_country'            
        )