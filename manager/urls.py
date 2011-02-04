from django.conf.urls.defaults import *
from manager.views import *

urlpatterns = patterns('',

    # Main web entrance.
    (r'^$', manager_main_page),

)

 
