from django import forms
from django.contrib.auth.forms import UserCreationForm
from captcha.fields import ReCaptchaField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, Div
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=200, required=True)
    captcha = ReCaptchaField(label="")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "",
                Div(
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "captcha",
                    css_id="register-form",
                ),
            ),
            ButtonHolder(Submit("submit", "Sign up", css_class="button white")),
        )

        
class ChangeUsernameForm(forms.ModelForm):
    username = forms.CharField(max_length=30, required=True, label="Username")
    action = forms.CharField(max_length=30)

    def clean_username(self):
        """ Cleaning username, checking if username exists in the
        db before changing it. """
        username = self.cleaned_data["username"]
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError(f"Username {username} is already in use.")
        return username

    def __init__(self, *args, **kwargs):
        super().__init__(*args, {})
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "",
                Div(
                    Field("action", value="user_form", type="hidden"),
                    Field("username", value=kwargs.get("user_name")),
                    css_id="change-username-form",
                ),
            )
        )

    class Meta:
        model = User
        fields = ("username",)


class ChangeEmailForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="Email")
    action = forms.CharField(max_length=30)

    def clean_email(self):
        """ Cleaning email, checking if it exists in the
        db before changing it. """
        email = self.cleaned_data["email"]
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError(f"{email} is already in use. Try another one.")
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, {})
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "",
                Div(
                    Field("action", value="email_form", type="hidden"),
                    Field("email", value=kwargs.get("user_email")),
                    css_id="change-email-form",
                ),
            )
        )

    class Meta:
        model = User
        fields = ("email",)


class RemoveAccountForm(forms.Form):
    username = forms.CharField(
        max_length=30, required=True, label="Enter your username to delete"
    )
    action = forms.CharField(max_length=30)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "",
                Div(
                    Field("action", value="remove_account", type="hidden"),
                    Field("username"),
                    css_id="remove-account-form",
                ),
            )
        )
