from django import forms
from django.conf import settings

class UploadFileForm(forms.Form):
    #Select the RDF file to upload (local file or via URL)
    file  = forms.FileField(label='From local machine (1)', required=False)
    url = forms.URLField(label='From URL (2)', required=False)
    #Select the database
    dataBases = forms.ChoiceField(label='Database to store the RDF file (3)', widget = forms.Select(), choices= settings.REVPROXY_SETTINGS)


class InsertOntology(forms.Form):
    name = forms.CharField(label='Ontology Name',required=True)
    url = forms.URLField(label='Ontology URI', required=True)
             
class SparqlQuery(forms.Form): 
    #Select the database
    db = forms.ChoiceField(choices= settings.REVPROXY_SETTINGS,
                            widget=forms.Select(),
                            label='Select DB to Query',
                            required=True)
    #Select the type of output
    output = forms.ChoiceField(choices= [('python', 'python object'), ('xml', 'xml'), ('json', 'json')],
                            widget=forms.Select(),
                            label='Query output format',
                            required=True)
    query = forms.CharField(widget=forms.Textarea(),label='Query String',required=True)

class UploadScriptForm(forms.Form):
    #Select the script to upload
    file  = forms.FileField(label='Script to upload', required=False)
    #Select the database
    dataBases = forms.ChoiceField(label='Database to store the script', widget = forms.Select(), choices= settings.REVPROXY_SETTINGS)

class addWebForm(forms.Form):
    name = forms.CharField(label='Web Name',required=True)
    url = forms.URLField(label='Web URI', required=True)
