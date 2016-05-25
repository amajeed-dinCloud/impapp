__author__ = 'Abdul'
from django.db import models

class User(models.Model):
    name = models.CharField(max_length=150, null=False)
    city = models.CharField(max_length=100, null=True)
    age = models.IntegerField(max_length=11, null=True)
    email = models.CharField(max_length=250, unique=True, null=True)
    img_url = models.URLField(blank=True, null=True)
    fb_id = models.CharField(unique=True, max_length=50, null=True)
    ins_id = models.CharField(unique=True, max_length=50, null=True)
    password = models.CharField(max_length=100, null=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s %s' % (self.name, self.email)


class Document(models.Model):
    IMG_TYPES = ((1, 'Profile Image'), (2, 'Rating Image'),)
    user = models.ForeignKey(User)
    image = models.FileField()
    type = models.IntegerField(default=1, choices=IMG_TYPES)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)


    def __unicode__(self):
        return u'%s %s' % (self.user.id, self.user.email)