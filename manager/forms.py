from django import forms

class UploadFileForm(forms.Form):
    file  = forms.FileField(required=False)
    url = forms.URLField(required=False)


class InsertOntology(forms.Form):
    name = forms.CharField(label='Ontology Name',required=True)
    url = forms.URLField(label='Ontology URI', required=True)

class SparqlQueryclass(forms.Form):
