__author__ = 'pborky'

from django import forms
from django.forms.widgets import  Input, PasswordInput

class LoginForm(forms.Form):

    username = forms.CharField (
        label='',
        max_length=100,
        required=True,
        widget=Input(attrs={'placeholder': 'Username'}),
    )
    password = forms.CharField (
        label='',
        max_length=100,
        required=True,
        widget=PasswordInput(attrs={'placeholder': 'Password'}),
    )
