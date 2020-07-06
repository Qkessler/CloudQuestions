from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from captcha.fields import ReCaptchaField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.layout import (Layout, Fieldset, ButtonHolder,
                                 Submit, Field, Div)


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=200, required=True)
    captcha = ReCaptchaField(label='')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                '',
                Div(
                    'username',
                    'email',
                    'password1',
                    'password2',
                    'captcha',
                    css_id="register-form")),
            ButtonHolder(
                Submit('submit', 'Signup', css_class='button white')
            )
        )


class ChangeUsernameForm(forms.Form):
    username = forms.CharField(max_length=30, required=True, label="")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                Div(
                    'username',
                    css_id="change-username-form")),
        )
