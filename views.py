
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.conf import settings

def main_page(request):
    response_dict = { 'tabla' : ("X","Y","Z"),  
    }
    return render_to_response('index.html', response_dict)

def logout_page(request):
  """
  Log users out and re-direct them to the main page.
  """
  logout(request)
  return HttpResponseRedirect('/') 
