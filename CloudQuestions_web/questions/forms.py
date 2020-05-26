from django import forms
from . import validators


class SearchForm(forms.Form):
    search_text = forms.CharField(label='Search topics', max_length=100)


class UploadFileForm(forms.Form):
    file = forms.FileField(validators=[validators.validate_markdown])


class CreateTopicForm(forms.Form):
    name = forms.CharField(max_length=30)


class CreateQuestionForm(forms.Form):
    question = forms.CharField(label='Question', max_length=200)
    answer = forms.CharField(label='Answer', max_length=400)
