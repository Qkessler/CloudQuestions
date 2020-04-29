from django import forms


class SearchForm(forms.Form):
    search_text = forms.CharField(label='Search topics', max_length=100)


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
