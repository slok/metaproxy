from django.conf.urls.defaults import *
from metaproxy.views import *
from django.contrib import admin
import manager
from manager.urls import *
admin.autodiscover()

urlpatterns = patterns('',
    
    #main page (directly the  proxy or a page with all the proxied sites??)
    (r'^$', main_page),
    
    #login/logout
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', logout_page),
    
    #admin
    (r'^admin/', include(admin.site.urls)),
    
    #manager
    (r'^manager/', include(manager.urls)),
    
    # Serve static content.
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': 'static'}),
)
