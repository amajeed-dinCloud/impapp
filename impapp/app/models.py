__author__ = 'Abdul'
from django.db import models
from uuid import uuid4
from django.db import IntegrityError


class User(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    name = models.CharField(max_length=150, null=False)
    city = models.CharField(max_length=100, null=True)
    age = models.IntegerField(null=True)
    email = models.CharField(max_length=250, unique=True, null=True)
    fb_id = models.CharField(unique=True, max_length=50, null=True)
    ins_id = models.CharField(unique=True, max_length=50, null=True)
    password = models.CharField(max_length=100, null=True)
    is_approved = models.BooleanField(default=0)
    is_public = models.BooleanField(default=1)
    profile_rating = models.FloatField(default=0, null=True)
    is_active = models.BooleanField(default=1)
    agent = models.CharField(max_length=20, null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s %s' % (self.name, self.email)

    def save(self, *args, **kwargs):
        if self.id:
            super(User, self).save(*args, **kwargs)
            return

        unique = False
        while not unique:
            try:
                self.id = uuid4().hex
                super(User, self).save(*args, **kwargs)
            except IntegrityError:
                self.id = uuid4().hex
            else:
                unique = True


class Document(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    IMG_TYPES = ((1, 'Profile Image'), (2, 'Rating Image'),)
    user = models.ForeignKey(User)
    image = models.FileField()
    type = models.IntegerField(default=1, choices=IMG_TYPES)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s %s' % (self.user.id, self.user.email)

    def save(self, *args, **kwargs):
        if self.id:
            super(Document, self).save(*args, **kwargs)
            return

        unique = False
        while not unique:
            try:
                self.id = uuid4().hex
                super(Document, self).save(*args, **kwargs)
            except IntegrityError:
                self.id = uuid4().hex
            else:
                unique = True


class Ratings(models.Model):
    rated_by = models.ForeignKey(User,related_name='rated_by')
    rated_profile = models.ForeignKey(User, related_name='rated_profile')
    rating = models.FloatField(default=0)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s %s %s' % (self.rated_by.name, self.rated_profile.name, self.rating)


class CustomAttributes(models.Model):
    desc = models.CharField(max_length=250,null=True)
    key = models.CharField(max_length=100, unique=True, null=False)
    val = models.CharField(max_length=1000)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s %s' % (self.key, self.val)