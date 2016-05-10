__author__ = 'Abdul'
from django.db import models

class Document(models.Model):
    image = models.FileField()
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)