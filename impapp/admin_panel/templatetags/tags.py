from django import template
register = template.Library()
from impapp.app.models import CustomAttributes
from django.core import serializers


def get_obj(pk):
    try:
        obj = CustomAttributes.objects.get(pk=int(pk))
        obj = serializers.serialize('json', [ obj, ])
        print obj
    except Exception, ex:
        print str(ex)
        obj = []
    return obj


get_obj = register.tag(get_obj)