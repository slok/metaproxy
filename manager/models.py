from django.db import models

# Create your models here.

class Ontology(models.Model):
    name = models.CharField(max_length=30, unique=True)
    url = models.CharField(max_length=200, unique=True)
    
    def __unicode__(self):
        return self.name

