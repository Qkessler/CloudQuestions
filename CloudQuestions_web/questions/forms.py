from django import forms
from . import validators


class SearchForm(forms.Form):
    search_text = forms.CharField(label='Search topics', max_length=100)


class UploadFileForm(forms.Form):
    file = forms.FileField(validators=[validators.validate_markdown])
