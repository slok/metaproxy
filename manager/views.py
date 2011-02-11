from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.template import RequestContext
from manager.models import Ontology
from manager.forms import *
from django.conf import settings
from utils.utils import *

@login_required
def manager_main_page(request):
    """
If users are authenticated, direct them to the main page. Otherwise,
take them to the login page.
"""
    return render_to_response('manager/index.html')

"""
TODOs: - Validation control (check if both of the fields in the form are empty)
       - Progress bar ?? :P
"""

def manager_rdf_upload_page(request):
   if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        # Check if the user has introduced an RDF file via the "url" 
        # field from the UploadFileForm class defined in 'forms.py'
        if request.POST.get('url'):
            if form.is_valid():
                urlFile = request.POST.get('url')
                filePath = settings.UPLOAD_URL
                # Retrieve an RDF file from an url
                download_rdf_file(urlFile,filePath)
                # In order to complete the filePath we need to get the 
                # name of the RDF file. To do that, first, we split the 
                # URL 
                parts = []
                for part in urlFile.split('/'):
                    parts.append(part)
                # Afterwards, we add to the filePath the last part of 
                # the splitted url which is the name of the RDF file
                filePath += parts[len(parts)-1]

        # If not, it means that the RDF file has been introduced via 
        # the "file" field 
        else:
            if form.is_valid():
                # Load an RDF file from the local machine 
                localFile = request.FILES['file']
                handle_uploaded_file(localFile)
                filePath = settings.UPLOAD_URL + localFile.name
                
        # Store the RDF file in the DB
        store_RDF(filePath,"root","darkside","rdfstore")
        return render_to_response('manager/thanks.html')
        
   else:
        form = UploadFileForm()
   return render_to_response('manager/RDF.html', {'form': form}, 
   context_instance=RequestContext(request))

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
    pageData = {'form': form,
    'ontologies':ontologies,
    'insert':insert,
    }
    #returning html, data, csrf token...
    return render_to_response('manager/ontology.html', pageData, context_instance=RequestContext(request))

def manager_sparql_queries_page(request):
    if request.method == 'POST':
        form = SparqlQuery(request.POST)
        if form.is_valid():
            #prepare the database and the query
            db = form.cleaned_data['db']
            query =  form.cleaned_data['query']
            #execute the query
            qres = sparql_query(query, "root", "larrakoetxea", db) 
            resultList = []
            #transform the query result to a list
            for row in qres.result:
                resultList.append((row[0].format(),row[1].format())) 
            #response with the html page and the results
            return render_to_response('manager/sparqlresult.html', {'resultList': resultList},context_instance=RequestContext(request))
    else:
        form = SparqlQuery()
        
    pageData = {'form': form,
    }
    #returning html, data, csrf token...
    return render_to_response('manager/sparql.html', pageData, context_instance=RequestContext(request))

def handle_uploaded_file(f):
    filePath = settings.UPLOAD_URL
    filePath += f.name
    destination = open(filePath, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()




  
  
