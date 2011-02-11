from django import forms
from django.conf import settings

class UploadFileForm(forms.Form):
    file  = forms.FileField(label='From local machine (1)', required=False)
    url = forms.URLField(label='From URL (2)', required=False)
    dataBases = forms.ChoiceField(label='Database to store the RDF file (3)', widget = forms.RadioSelect(), choices= settings.REVPROXY_SETTINGS)


class InsertOntology(forms.Form):
    name = forms.CharField(label='Ontology Name',required=True)
    url = forms.URLField(label='Ontology URI', required=True)
<<<<<<< HEAD

# class SparqlQueryclass(forms.Form):
=======
                            
class SparqlQuery(forms.Form): 
    #radio button with the databases
    db = forms.ChoiceField(choices= settings.REVPROXY_SETTINGS,
                            widget=forms.RadioSelect(),
                            label='Data Base',
                            required=True)
    query = forms.CharField(widget=forms.Textarea(),label='Query String',required=True)
>>>>>>> 8f8aeeef7319ba27a726be75afd07e1c41731f07
