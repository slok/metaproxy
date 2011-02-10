from django import forms
from django.conf import settings

class UploadFileForm(forms.Form):
    file  = forms.FileField(required=False)
    url = forms.URLField(required=False)


class InsertOntology(forms.Form):
    name = forms.CharField(label='Ontology Name',required=True)
    url = forms.URLField(label='Ontology URI', required=True)
                            
class SparqlQuery(forms.Form): 
    #radio button with the databases
    db = forms.ChoiceField(choices= settings.REVPROXY_SETTINGS,
                            widget=forms.RadioSelect(),
                            label='Data Base',
                            required=True)
    query = forms.CharField(widget=forms.Textarea(),label='Query String',required=True)
