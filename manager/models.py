from django.db import models
from django.contrib import admin
from django.db import models
# Create your models here.

class Ontology(models.Model):
    name = models.CharField(max_length=30, unique=True)
    url = models.CharField(max_length=200, unique=True)
    
    def __unicode__(self):
        return self.name

class RequestSession(models.Model):
    """ simple request session models. All the session is saved on the
    disk """

    sid = models.CharField(max_length=4096)
    executed = models.DateTimeField(auto_now=True)
    request_id = models.CharField(max_length=255)
    store_path = models.CharField(max_length=255)

    def __str__(self):
        return "%s - %s" % (self.executed, self.request_id)

admin.site.register(RequestSession)
