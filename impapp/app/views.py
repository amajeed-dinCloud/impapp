__author__ = 'Abdul'
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from models import Document

@csrf_exempt
def test(request):
    image = request.FILES.get('image')
    print len(image)
    newdoc = Document(image=image)
    newdoc.save()
    print newdoc.image.url
    newdoc.delete()
    return HttpResponse("Service is running")