__author__ = 'Abdul'
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from models import Document, User
import json
import requests
from impapp import configs as conf
import traceback
from impapp import util_functions


@csrf_exempt
def sign_up(request):
    out_dict = {"code": 500, "status": "error", "message": ""}
    if request.method == "POST":
        try:
            name = request.POST.get('name')
            age = request.POST.get('age')
            city = request.POST.get('city')
            email = request.POST.get('email')
            img_url = request.POST.get('img_url')
            fb_id = request.POST.get('fb_id')
            ins_id = request.POST.get('ins_id')
            if not email and not ins_id and not fb_id or not name:
               out_dict["message"] = "Name, email, fb_id or ins_id  is missing."
            else:
                user_obj = is_user_exists(email, fb_id, ins_id)
                if user_obj:
                    out_dict["message"]="User already exists"
                else:
                    user_obj = User()
                    user_obj.name = name
                    user_obj.city = city
                    if util_functions.validate_email(email):
                        user_obj.email = email
                    if util_functions.validate_age(age):
                        user_obj.age = int(age)
                    if util_functions.validate_url(img_url):
                        user_obj.img_url = img_url
                    if fb_id:
                        user_obj.fb_id=fb_id
                    if ins_id:
                        user_obj.ins_id=ins_id
                    if city:
                        user_obj.city = city
                    user_obj.save()
                    out_dict["user"] = make_user_response(user_obj)
                    out_dict["code"] = 200
                    out_dict["status"] = "ok"
        except Exception, ex:
            print traceback.print_exc(5)
            out_dict["message"] = str(ex)
    else:
        out_dict = {"code": 405, "status": "error", "message": "Method not allowed."}

    return HttpResponse(json.dumps(out_dict))


def is_user_exists(email, fb_id, ins_id):
    user_obj = None
    if email:
        user_obj = User.objects.filter(email=email)
    elif fb_id:
        user_obj = User.objects.filter(email=fb_id)
    elif ins_id:
        user_obj = User.objects.filter(email=ins_id)

    if user_obj:
        user_obj = user_obj[0]

    return user_obj


@csrf_exempt
def login(request):
    out_dict = {"code": 500, "status": "error", "message": ""}
    if request.method == "POST":
        try:
            email = request.POST.get('email')
            fb_id = request.POST.get('fb_id')
            ins_id = request.POST.get('ins_id')
            password = request.POST.get('password')
            if not email and not ins_id and not fb_id:
               out_dict["message"] = "Email, fb_id or ins_id is missing."
            else:
                user_obj = is_user_exists(email, fb_id, ins_id)
                if user_obj:
                    if email:
                        if user_obj.email == email and user_obj.password == password:
                            out_dict["user"] = make_user_response(user_obj)
                            out_dict["code"] = 200
                            out_dict["status"] = "ok"
                        else:
                            out_dict["message"] = "User email and password don't match."
                    else:
                        out_dict["user"] = make_user_response(user_obj)
                        out_dict["code"] = 200
                        out_dict["status"] = "ok"
                else:
                    out_dict["message"] = "User does not exists."
        except Exception, ex:
            out_dict["message"] = str(ex)
    else:
        out_dict = {"code": 405, "status": "error", "message": "Method not allowed."}

    return HttpResponse(json.dumps(out_dict))


@csrf_exempt
def update_profile(request):
    out_dict = {"code": 500, "status": "error", "message": ""}
    if request.method == "POST":
        try:
            name = request.POST.get('name')
            age = request.POST.get('age')
            city = request.POST.get('city')
            email = request.POST.get('email')
            fb_id = request.POST.get('fb_id')
            ins_id = request.POST.get('ins_id')
            img_url = request.POST.get('img_url')

            if not email and not ins_id and not fb_id:
               out_dict["message"] = "Email, fb_id or ins_id is missing."
            else:
                user_obj = is_user_exists(email, fb_id, ins_id)
                if not user_obj:
                    out_dict["message"] = "User is not found."
                else:
                    user_obj = user_obj[0]
                    if name:
                        user_obj.name = name
                    if util_functions.validate_age(age):
                        user_obj.age = int(age)
                    if city:
                        user_obj.city = city
                    if not user_obj.email and util_functions.validate_email(email):
                        user_obj.email = email
                    if not user_obj.fb_id and fb_id:
                        user_obj.fb_id = fb_id
                    if not user_obj.ins_id and ins_id:
                        user_obj.ins_id = ins_id

                    user_obj.save()

                    out_dict["user"] = make_user_response(user_obj)
                    out_dict["code"] = 200
                    out_dict["status"] = "ok"
                    out_dict["message"] = ""
        except Exception, ex:
            print traceback.print_exc(5)
            out_dict["message"] = str(ex)
    else:
        out_dict = {"code": 405, "status": "error", "message": "Method not allowed."}

    return HttpResponse(json.dumps(out_dict))







def make_user_response(user_obj):
    return {"name": user_obj.name, "age": user_obj.age, "city": user_obj.city, "email": user_obj.email,
            "img_url": user_obj.img_url, "fb_id": user_obj.fb_id, "ins_id": user_obj.ins_id}


@csrf_exempt
def upload_image(request):
    out_dict = {"code": 500, "status": "error", "message": ""}
    if request.method == "POST":
        image = request.FILES.get('image')
        email = request.POST.get('email')
        fb_id = request.POST.get('fb_id')
        ins_id = request.POST.get('ins_id')
        type = request.POST.get('type', '2')
        if not email and not ins_id and not fb_id and not image:
            out_dict["message"] = "Email, fb_id or ins_id is missing."
        else:
            user_obj = is_user_exists(email, fb_id, ins_id)
            if not user_obj:
                out_dict["message"] = "User not found."
            else:
                if type == '1':
                    img_obj = Document.objects.filter(image=image, user=user_obj, type=1)
                    if img_obj:
                        img_obj = img_obj[0]
                        img_obj.image.delete()
                    else:
                        img_obj = Document()
                    img_obj.image = image
                    img_obj.user = user_obj
                    img_obj.save()
                    out_dict["img_url"] = str(img_obj.image.url)

                elif type == '2':
                    img_obj = Document.objects.filter(image=image, user=user_obj, type=2)
                    if len(img_obj) <= conf.USER_MAX_IMAGES:
                        Document.objects.create(image=image, user=user_obj, type=2)
                        img_obj.image = image
                        img_obj.user = user_obj
                        img_obj.save()
                        out_dict["img_url"] = str(img_obj.image.url)
                    else:
                        out_dict["message"] = "Max no of images are already submitted."

    else:
        out_dict = {"code": 405, "status": "error", "message": "Method not allowed."}

    return HttpResponse(json.dumps(out_dict))


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

