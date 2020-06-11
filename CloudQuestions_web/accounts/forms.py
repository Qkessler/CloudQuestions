from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from captcha.fields import ReCaptchaField
from crispy_forms.helper import FormHelper


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=200, required=True)
    captcha = ReCaptchaField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )
