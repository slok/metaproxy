from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.template import RequestContext
from manager.models import Ontology
from manager.forms import *
from django.conf import settings

@login_required
def manager_main_page(request):
    """
If users are authenticated, direct them to the main page. Otherwise,
take them to the login page.
"""
    return render_to_response('manager/index.html')


def manager_rdf_upload_page(request):
   if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return render_to_response('manager/thanks.html')
   else:
        form = UploadFileForm()
   return render_to_response('manager/RDF.html', {'form': form}, context_instance=RequestContext(request))

def manager_ontologies_page(request):
    insert = False
    if request.method == 'POST':
        form = InsertOntology(request.POST)
        if form.is_valid():
            #get data from the form
            n = form.cleaned_data['name']
            u = form.cleaned_data['url']
            # create the model object
            ont = Ontology(name=n, url=u)
            try:
                #save in the DB the new object, is in a try to capture 
                #the exception if there is alredy an object 
                ont.save()
                insert=True
            except:
                pass
            #create a blank form again to return to the ontology page    
            form = InsertOntology()
    else:
        form = InsertOntology()
    
    #get all the objects from the ontology table
    ontologies = []
    for e in  Ontology.objects.all():
        ontologies.append((e.name, e.url))
        
    #the data for the html (variables...)
    pageDate = {'form': form,
    'ontologies':ontologies,
    'insert':insert,
    }
    #returning html, data, csrf token...
    return render_to_response('manager/ontology.html', pageDate, context_instance=RequestContext(request))

def manager_sparql_queries_page(request):
  pass

def manager_sparql_results_page(request):
  pass

def manager_proxied_sites_page(request):
  pass

def handle_uploaded_file(f):
    filePath = settings.UPLOAD_URL
    filePath += f.name
    destination = open(filePath, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()




  
  
