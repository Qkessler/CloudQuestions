from django import forms
from . import validators
from captcha.fields import ReCaptchaField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class SearchForm(forms.Form):
    search_text = forms.CharField(
        label='', max_length=100, widget=forms.TextInput(
            attrs={'class': 'search_form',
                   'placeholder': 'Search...'}))


class UploadFileForm(forms.Form):
    file = forms.FileField(validators=[validators.validate_markdown],
                           label="",
                           widget=forms.FileInput(
                               attrs={'id': 'file_upload'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'file_upload-form'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'

        self.helper.add_input(Submit('submit', 'Submit'))


class CreateTopicForm(forms.Form):
    name = forms.CharField(max_length=30)
    captcha = ReCaptchaField(label='')


class CreateQuestionForm(forms.Form):
    question = forms.CharField(label='Question', max_length=200)
    answer = forms.CharField(label='Answer', max_length=400)
