from django import forms


class SearchForm(forms.Form):
    search_text = forms.CharField(label='Search topics', max_length=100)


class UploadFileForm(forms.Form):
    file = forms.FileField()
