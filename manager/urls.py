from django.conf.urls.defaults import *
from manager.views import *

urlpatterns = patterns('',

    # Main web entrance.
    (r'^$', manager_main_page),
    (r'^rdf/$', manager_rdf_upload_page),
    (r'^ontologies/$', manager_ontologies_page),
    (r'^sparql/$', manager_sparql_queries_page),
    (r'^scripts/$', manager_scripts_page),
    (r'^scripts/(?P<id>\w+)/$', manager_scripts_code_page),
    (r'^addweb/$', manager_addweb_page),
    (r'^addweb/(?P<id>\w+)/$', manager_addweb_delete_page),

)

 
