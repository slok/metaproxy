from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.template import RequestContext
from manager.models import Ontology
from manager.forms import *
from django.conf import settings
from utils.utils import *
import xml.dom.minidom

@login_required
def manager_main_page(request):
    """
If users are authenticated, direct them to the main page. Otherwise,
take them to the login page.
"""
    return render_to_response('manager/index.html')

"""
TODOs: - Validation control:
            - Check the types of the uploaded files (e.g.: if the 
              uploaded file in the Scripts page is eventually an 
              script file)
            - Check if the form fields are empty
       - Progress bar ?? :P
       - Revise the manager_rdf_upload_page. It doesn't store the RDF
         file properly in the DB.
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
                
        # [FIXME] Store the RDF file in the DB (doesn't work PROPERLY!)
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
            output =  form.cleaned_data['output']
            #execute the query
            qres = sparql_query(query, "root", "larrakoetxea", db, output) 
            resultList = []
            #transform the query result to a list if is python
            if output == "python":
                for row in qres.result:
                    resultList.append((row[0].format(),row[1].format()))
            elif(output == "xml"):
                #pretiffy the XML with indentation
                xmlQres = xml.dom.minidom.parseString(qres)
                resultList = xmlQres.toprettyxml()
            else: 
                resultList = qres
            #response with the html page and the results
            return render_to_response('manager/sparqlresult.html', {'resultList': resultList, 'output':output},context_instance=RequestContext(request))
    else:
        form = SparqlQuery()
        
    pageData = {'form': form,
    }
    #returning html, data, csrf token...
    return render_to_response('manager/sparql.html', pageData, context_instance=RequestContext(request))

def manager_scripts_page(request):
    if request.method == 'POST':
        form = UploadScriptForm(request.POST, request.FILES)
        if form.is_valid(): 
            localFile = request.FILES['file']
            db = form.cleaned_data['dataBases']
            handle_uploaded_script(localFile, db)
        return render_to_response('manager/thanks.html')
        
    else:
        form = UploadScriptForm()
    return render_to_response('manager/scripts.html', {'form': form,
    'scriptUrls': settings.REVPROXY_SETTINGS}, 
    context_instance=RequestContext(request))

def manager_scripts_code_page(request, id):
    strScript = read_file_Script(id)
    pageData = {
    'strScript': strScript,
    }
    return render_to_response('manager/scriptsCode.html', pageData)

def handle_uploaded_file(f):
    filePath = settings.UPLOAD_URL
    filePath += f.name
    destination = open(filePath, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

def handle_uploaded_script(s, db):
    filePath = settings.UPLOAD_URL_SCRIPTS
    filePath += db
    filePath += '/'
    filePath += 'ModifyBody.py'    
    destination = open(filePath, 'wb+')
    for chunk in s.chunks():
        destination.write(chunk)
    destination.close()

def read_file_Script(script):
    filePath = settings.UPLOAD_URL_SCRIPTS
    filePath += script
    filePath += '/'
    filePath += 'ModifyBody.py'
    return read_file(filePath)
    
def read_file(filePath):
    return open(filePath, 'r').read()




  
  