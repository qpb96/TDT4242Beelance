from django import forms
from user.models import Profile

class NameForm(forms.ModelForm):
#    last_name = forms.CharField(label='Your name', max_length=100)

    class Meta:
        model = Profile
        fields = ('phone_number',)