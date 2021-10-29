from django.db import models

# Create your models here.
from django.db import models

class AssetRelation(models.Model):
    relation_type = models.CharField(max_length=32, default="component")
    name = models.CharField(max_length=32, default="component")
    lastname = models.CharField(max_length=32, default="component")
    order = models.IntegerField(null=True, blank=True)

