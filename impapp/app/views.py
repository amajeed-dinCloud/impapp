__author__ = 'Abdul'
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from models import Document
import json
import requests
from impapp import configs as conf


@csrf_exempt
def test(request):
    image = request.FILES.get('image')
    print len(image)
    newdoc = Document(image=image)
    newdoc.save()
    print newdoc.image.url
    newdoc.delete()

    return HttpResponse("Service is running")

def isworking(request):
    return  HttpResponse("*IS WORKING*")


def redirect_insta(request):
    out = {"code": 501, "error_type": "general error", "error_message": "there is some issue on server auth code is missing."}
    code = request.GET.get('code')
    if code:
        r = requests.post(conf.URL, data={'client_id': conf.CLIENT_ID, 'client_secret': conf.CLIENT_SECRET,'code': code,
                                          'grant_type': 'authorization_code', 'redirect_uri': conf.REDIRECT_URI})
        out = r.text
    else:
        out = json.dumps(out)

    return HttpResponse(out)