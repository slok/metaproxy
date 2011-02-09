from django import forms

class UploadFileForm(forms.Form):
    name = forms.CharField(required=True)

