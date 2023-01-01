from django.forms import ModelForm
from django import forms
from register.models import *
from register.views import *
class RegistrationForm(forms.Form):
    email = forms.EmailField()
    usertype = forms.CharField()

