from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from projects.models import ProjectCategory

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



class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    company = forms.CharField(max_length=30, required=False, help_text= 'Here you can add your company.')
    phone_number = forms.CharField(max_length=50, required=False)

    street_address = forms.CharField(max_length=50, required=False)
    city = forms.CharField(max_length=50, required=False)
    state = forms.CharField(max_length=50, required=False)
    postal_code = forms.CharField(max_length=10, required=False)
    country = forms.CharField(max_length=50, required=False)
    categories = forms.ModelMultipleChoiceField(queryset=ProjectCategory.objects.all(), required=False, help_text='Hold down "Control", or "Command" on a Mac, to select more than one.')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'categories', 'company' ,  'phone_number', 'street_address', 'city', 'state', 'postal_code', 'country' )