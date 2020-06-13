from django import forms
from . import validators
from captcha.fields import ReCaptchaField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.layout import (Layout, Fieldset, ButtonHolder,
                                 Submit, Field, Div)


class SearchForm(forms.Form):
    search_text = forms.CharField(
        label='', max_length=100, widget=forms.TextInput(
            attrs={'class': 'search_form',
                   'placeholder': 'Search...'}))


class UploadFileForm(forms.Form):
    file_upload = forms.FileField(validators=[validators.validate_markdown],
                                  label="",
                                  widget=forms.FileInput(
                                      attrs={'id': 'file_upload'}))


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
        max_length=400,
        required=True,
        widget=forms.Textarea)
    captcha = ReCaptchaField(label='')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                '',
                'name',
                'question',
                'answer',
                'captcha'),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='button white')
            )
        )


class ExampleForm(forms.Form):
    like_website = forms.TypedChoiceField(
        label="Do you like this website?",
        choices=((1, "Yes"), (0, "No")),
        coerce=lambda x: bool(int(x)),
        widget=forms.RadioSelect,
        initial='1',
        required=True,
    )

    favorite_food = forms.CharField(
        label="What is your favorite food?",
        max_length=80,
        required=True,
    )

    favorite_color = forms.CharField(
        label="What is your favorite color?",
        max_length=80,
        required=True,
    )

    favorite_number = forms.IntegerField(
        label="Favorite number",
        required=False,
    )

    notes = forms.CharField(
        label="Additional notes or feedback",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = '#'

        self.helper.add_input(Submit('submit', 'Submit'))
