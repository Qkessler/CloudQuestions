from . import validators
from django import forms
from captcha.fields import ReCaptchaField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.layout import (Layout, Fieldset, ButtonHolder,
                                 Field, Div, Submit)


class SearchForm(forms.Form):
    search_text = forms.CharField(
        label='', max_length=100, widget=forms.TextInput(
            attrs={'class': 'search_form',
                   'placeholder': 'Search...'}))


class UploadFileForm(forms.Form):
    file = forms.FileField(validators=[validators.validate_markdown],
                           label="")
    action = forms.CharField(max_length=30)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                '',
                Div(
                    Field('action', value="upload", type="hidden"),
                    Field('file', css_id="file-upload", name="file_upload"),
                    css_id="file-upload-form")),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='btn btn-danger',
                       css_id="file-button")
            )
        )


class CreateTopicForm(forms.Form):
    name = forms.CharField(
        label='Topic name',
        max_length=30,
        required=True)
    question = forms.CharField(
        label='Question',
        max_length=200,
        required=True,
        widget=forms.Textarea)
    answer = forms.CharField(
        label='Answer',
        max_length=600,
        required=True,
        widget=forms.Textarea)
    captcha = ReCaptchaField(label='')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                '',
                Div(
                    'name',
                    'question',
                    'answer',
                    'captcha',
                    css_id="create-topic-form")),
            ButtonHolder(
                Submit('submit', 'Add question', css_class='button white')
            )
        )


class CreateTopicFormId(forms.Form):
    question = forms.CharField(
        label='Question',
        max_length=200,
        required=True,
        widget=forms.Textarea)
    answer = forms.CharField(
        label='Answer',
        max_length=600,
        required=True,
        widget=forms.Textarea)
    captcha = ReCaptchaField(label='')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                '',
                Div(
                    'question',
                    'answer',
                    'captcha',
                    css_id="create-topic-form")),
            ButtonHolder(
                Submit('submit', 'Add question', css_class='button white')
            )
        )
