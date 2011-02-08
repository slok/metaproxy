from django import forms

class UploadFileFormForm(forms.Form):
    name = forms.CharField(required=True)

