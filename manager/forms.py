from django import forms

class UploadFileForm(forms.Form):
    file  = forms.FileField(required=False)
    url = forms.URLField(required=False)


