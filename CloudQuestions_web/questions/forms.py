from django import forms
from . import validators
from captcha.fields import ReCaptchaField


class SearchForm(forms.Form):
    search_text = forms.CharField(
        label='', max_length=100, widget=forms.TextInput(
            attrs={'class': 'search_form',
                   'placeholder': 'Search...'}))


class UploadFileForm(forms.Form):
    file = forms.FileField(validators=[validators.validate_markdown],
                           label="",
                           widget=forms.FileInput(
                               attrs={'id': 'file_upload',
                                      'name': 'file'}))


class CreateTopicForm(forms.Form):
    name = forms.CharField(max_length=30)
    captcha = ReCaptchaField(label='')


class CreateQuestionForm(forms.Form):
    question = forms.CharField(label='Question', max_length=200)
    answer = forms.CharField(label='Answer', max_length=400)
