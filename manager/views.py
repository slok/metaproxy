from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

@login_required
def manager_main_page(request):
    """
If users are authenticated, direct them to the main page. Otherwise,
take them to the login page.
"""
    return render_to_response('manager/index.html')


def manager_rdf_upload_page(request):
  return render_to_response('manager/RDF.html')

def manager_ontologies_upload_page(request):
  pass

def manager_sparql_queries_page(request):
  pass

def manager_sparql_results_page(request):
  pass

def manager_proxied_sites_page(request):
  pass

def handle_uploaded_file(f):
    destination = open('some/file/name.txt', 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
################################################################
"""

"""
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render_to_response('manager/RDF.html')
  
 
  
  
