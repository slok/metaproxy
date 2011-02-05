from django.conf.urls.defaults import *
from manager.views import *

urlpatterns = patterns('',

    # Main web entrance.
    (r'^$', manager_main_page),
    (r'^rdf/$', manager_rdf_upload_page),
    (r'^ontologies/$', manager_ontologies_upload_page),
    (r'^sparql/$', manager_sparql_queries_page),
    (r'^sparql/result/$', manager_sparql_results_page),
    (r'^proxied$', manager_proxied_sites_page),

)

 
