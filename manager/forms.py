from django import forms
from django.conf import settings

class UploadFileForm(forms.Form):
    file  = forms.FileField(label='From local machine (1)', required=False)
    url = forms.URLField(label='From URL (2)', required=False)
    dataBases = forms.ChoiceField(label='Database to store the RDF file (3)', widget = forms.RadioSelect(), choices= settings.REVPROXY_SETTINGS)


class InsertOntology(forms.Form):
    name = forms.CharField(label='Ontology Name',required=True)
    url = forms.URLField(label='Ontology URI', required=True)

# class SparqlQueryclass(forms.Form):
