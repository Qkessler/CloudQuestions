from django import forms
from django.contrib.auth.forms import UserCreationForm
from captcha.fields import ReCaptchaField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (Layout, Fieldset, ButtonHolder,
                                 Submit, Field, Div, HTML)


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
    username = forms.CharField(max_length=30, required=True, label="Username")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, {})
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                '',
                Div(
                    Field('username', value=kwargs.get('user_name')),
                    css_id="change-username-form")
            )
        )
