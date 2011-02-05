from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

@login_required
def manager_main_page(request):
    """
If users are authenticated, direct them to the main page. Otherwise,
take them to the login page.
"""
    return render_to_response('manager/index.html')


def manager_rdf_upload_page(request):
  pass

def manager_ontologies_upload_page(request):
  pass

def manager_sparql_queries_page(request):
  pass

def manager_sparql_results_page(request):
  pass

def manager_proxied_sites_page(request):
  pass