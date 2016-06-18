__author__ = 'Abdul'
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from impapp.update_ratings import refresh_ratings
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from impapp.app.models import User
from impapp.app.functions import *
import json
from impapp import util_functions

@login_required
def is_working(request):
    return render_to_response('dashboard.html', {'request': request, 'menu': 'dashboard'},
                              context_instance=RequestContext(request))
    # return HttpResponse("*IS WORKING*")


@login_required
def update_all_ratings(request):
    update_rows = refresh_ratings()
    return render_to_response('refresh_ratings.html', {'request': request, 'menu': 'refresh_ratings',"update_rows": update_rows},
                              context_instance=RequestContext(request))

@login_required
def custom_attributes_list(request):
    return render_to_response('custom_attributes.html', {'request': request, 'menu': 'custom_attributes'},
                              context_instance=RequestContext(request))

@login_required
def top_ten(request):
    top_ten_users = User.objects.filter(is_approved=1, is_public=1, is_active=1).order_by('-profile_rating')[:10]
    return render_to_response('top_ten.html', {'request': request, 'menu': 'top_ten',
                                                         'top_ten_users': top_ten_users},
                              context_instance=RequestContext(request))

def del_user(request):
    try:
        redirect_url = request.GET["redirect_url"]
        user_id = request.GET["user_id"]
        print redirect_url
        user_obj = User.objects.get(id=user_id)
        delete_images(user_obj)
        user_obj.delete()
        msg = "User has been delete successfully."
    except Exception,ex:
        print ex
        msg = str(ex)

    return HttpResponseRedirect(redirect_url+"?msg="+msg)


def get_user(request):
    user_dict = {}
    try:
        user_id = request.GET["user_id"]
        user_obj = User.objects.get(id=user_id)
        user_dict = make_user_response(user_obj)
    except Exception, ex:
        print str(ex)
    return HttpResponse (json.dumps(user_dict))



def update_user(request):
    print request.path
    try:
        redirect_url = request.POST["redirect_url"]
        user_id = request.POST["user_id"]
        name = request.POST["name"]
        city = request.POST.get('city')
        age = request.POST.get('age')
        password = request.POST.get('password')

        is_active = request.POST.get('is_active')
        is_active = True if is_active else False

        is_public = request.POST.get('is_public')
        is_public = True if is_public else False

        is_approved = request.POST.get('is_approved')
        is_approved = True if is_approved else False

        user_obj = User.objects.get(id=user_id)
        user_obj.name=name
        user_obj.city = city
        if util_functions.validate_age(age):
            user_obj.age = age

        user_obj.password = password

        user_obj.is_active = is_active
        user_obj.is_public = is_public
        user_obj.is_approved = is_approved

        user_obj.save()
        msg = "User Updated successfully."

    except Exception, ex:
        msg = str(ex)
    return HttpResponseRedirect(redirect_url+"?msg="+msg)