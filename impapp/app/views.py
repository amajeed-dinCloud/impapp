__author__ = 'Abdul'
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from models import Document, User, Ratings
import json
import requests
import traceback
from impapp import util_functions
from impapp import configs as conf
from impapp.app.functions import *

@csrf_exempt
def sign_up(request):
    out_dict = {"code": 500, "status": "error", "message": ""}
    if request.method == "POST":
        try:
            name = request.POST.get('name')
            age = request.POST.get('age')
            city = request.POST.get('city')
            email = request.POST.get('email')
            fb_id = request.POST.get('fb_id')
            ins_id = request.POST.get('ins_id')
            password = request.POST.get('password')
            if not email and not ins_id and not fb_id or not name:
                out_dict["message"] = "Name, email, fb_id or ins_id  is missing."
            else:
                user_obj = is_user_exists(email, fb_id, ins_id)
                if user_obj:
                    out_dict["message"] = "User already exists"
                else:
                    user_obj = User()
                    user_obj.name = name
                    user_obj.city = city
                    if email and util_functions.validate_email(email):
                        user_obj.email = email
                        if not fb_id and not ins_id and not password:
                            out_dict["message"] = "Please provide a password"
                            return HttpResponse(json.dumps(out_dict))
                        else:
                            user_obj.password = password
                    if util_functions.validate_age(age):
                        user_obj.age = int(age)
                    if fb_id:
                        user_obj.fb_id = fb_id
                    if ins_id:
                        user_obj.ins_id = ins_id
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
                    if email and not fb_id and not ins_id:
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
            img_id = request.POST.get('img_id')

            if not email and not ins_id and not fb_id:
               out_dict["message"] = "Email, fb_id or ins_id is missing."
            else:
                user_obj = is_user_exists(email, fb_id, ins_id)
                if not user_obj:
                    out_dict["message"] = "User is not found."
                else:
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

                    if img_id:
                        update_profile_image_internal(user_obj, img_id)

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


@csrf_exempt
def upload_image(request):
    out_dict = {"code": 500, "status": "error", "message": ""}
    if request.method == "POST":
        try:
            image = request.FILES['image']
            email = request.POST.get('email')
            fb_id = request.POST.get('fb_id')
            ins_id = request.POST.get('ins_id')
            type = request.POST.get('type', '2')

            if not email and not ins_id and not fb_id:
                out_dict["message"] = "Image, Email, fb_id or ins_id is missing."

            else:
                user_obj = is_user_exists(email, fb_id, ins_id)
                if not user_obj:
                    out_dict["message"] = "User not found."
                else:
                    if type == '1':
                        img_obj = Document.objects.filter(user=user_obj, type=type)
                        if img_obj:
                            img_obj = img_obj[0]
                            img_obj.image.delete()
                        else:
                            img_obj = Document()
                        img_obj.image = image
                        img_obj.user = user_obj
                        img_obj.save()
                        out_dict = make_image_dict(img_obj)
                        out_dict["code"] = 200
                        out_dict["status"] = "ok"

                    elif type == '2':
                        img_objs = Document.objects.filter(user=user_obj)
                        if not img_objs:
                            type = 1
                        if len(img_objs) <= conf.USER_MAX_IMAGES:
                            img_obj = Document.objects.create(image=image, user=user_obj, type=type)
                            out_dict = make_image_dict(img_obj)
                            out_dict["code"] = 200
                            out_dict["status"] = "ok"
                        else:
                            out_dict["message"] = "Max no of images are already submitted."
        except Exception, ex:
            out_dict = {"code": 500, "status": "error", "message": str(ex)}

    else:
        out_dict = {"code": 405, "status": "error", "message": "Method not allowed."}

    return HttpResponse(json.dumps(out_dict))


@csrf_exempt
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

@csrf_exempt
def update_profile_image(request):
    out_dict = {"code": 500, "status": "error", "message": ""}
    if request.method == "POST":
        try:
            email = request.POST.get('email')
            fb_id = request.POST.get('fb_id')
            ins_id = request.POST.get('ins_id')
            img_id = request.POST['img_id']

            if not email and not ins_id and not fb_id:
                out_dict["message"] = "Image, Email, fb_id or ins_id is missing."

            else:
                user_obj = is_user_exists(email, fb_id, ins_id)
                if not user_obj:
                    out_dict["message"] = "User not found."
                else:
                    status = update_profile_image_internal(user_obj, img_id)
                    if status:
                        out_dict["user_images"] = make_user_images(user_obj)
                        out_dict["code"] = 200
                        out_dict["status"] = "ok"
                    else:
                        out_dict["message"] = "No image found to update."
        except Exception, ex:
            out_dict = {"code": 500, "status": "error", "message": str(ex)}

    else:
        out_dict = {"code": 405, "status": "error", "message": "Method not allowed."}

    return HttpResponse(json.dumps(out_dict))


@csrf_exempt
def delete_user_image(request):
    out_dict = {"code": 500, "status": "error", "message": ""}
    if request.method == "POST":
        try:
            email = request.POST.get('email')
            fb_id = request.POST.get('fb_id')
            ins_id = request.POST.get('ins_id')
            img_ids = request.POST.getlist('img_id')

            if not email and not ins_id and not fb_id:
                out_dict["message"] = "Email, fb_id or ins_id is missing."
            else:
                user_obj = is_user_exists(email, fb_id, ins_id)
                if not user_obj:
                    out_dict["message"] = "User not found."
                else:
                    status = delete_images(user_obj, img_ids)
                    if status:
                        out_dict["user_images"] = make_user_images(user_obj)
                        out_dict["code"] = 200
                        out_dict["status"] = "ok"
                    else:
                        out_dict["message"] = "No image found to delete."
        except Exception, ex:
            out_dict = {"code": 500, "status": "error", "message": str(ex)}

    else:
        out_dict = {"code": 405, "status": "error", "message": "Method not allowed."}

    return HttpResponse(json.dumps(out_dict))

@csrf_exempt
def delete_user(request):
    out_dict = {"code": 500, "status": "error", "message": ""}
    if request.method == "POST":
        try:
            email = request.POST.get('email')
            fb_id = request.POST.get('fb_id')
            ins_id = request.POST.get('ins_id')
            if not email and not ins_id and not fb_id:
                out_dict["message"] = "Email, fb_id or ins_id is missing."

            else:
                user_obj = is_user_exists(email, fb_id, ins_id)
                if not user_obj:
                    out_dict["message"] = "User not found."
                else:
                    delete_images(user_obj)
                    user_obj.delete()
                    out_dict["code"] = 200
                    out_dict["status"] = "ok"
        except Exception, ex:
            out_dict = {"code": 500, "status": "error", "message": str(ex)}

    else:
        out_dict = {"code": 405, "status": "error", "message": "Method not allowed."}

    return HttpResponse(json.dumps(out_dict))


@csrf_exempt
def rate_user(request):
    out_dict = {"code": 500, "status": "error", "message": ""}
    if request.method == "POST":
        try:
            rated_by = request.POST.get('rated_by')
            rated_profile = request.POST.get('rated_profile')
            rating = request.POST.get('rating')
            if not rated_by or not rated_profile or not rating:
                out_dict["message"] = "Mandatory param is missing."
            elif rated_by != rated_profile:
                is_valid_rating = util_functions.validate_float(rating)
                if is_valid_rating:
                    rated_by = User.objects.get(id=rated_by)
                    rated_profile = User.objects.get(id=rated_profile)
                    rating = float(rating)
                    is_rated = Ratings.objects.filter(rated_by=rated_by, rated_profile=rated_profile)
                    rating_obj = is_rated[0] if is_rated else Ratings()
                    rating_obj.rated_profile = rated_profile
                    rating_obj.rated_by = rated_by
                    rating_obj.rating = rating
                    rating_obj.save()
                    out_dict["status"] = "ok"
                    out_dict["code"] = 200
                else:
                    out_dict["message"] = "Rating is not valid."
            else:
                out_dict["message"] = "Self rating not allowed."
        except Exception, ex:
            out_dict = {"code": 500, "status": "error", "message": str(ex)}

    else:
        out_dict = {"code": 405, "status": "error", "message": "Method not allowed."}

    return HttpResponse(json.dumps(out_dict))

