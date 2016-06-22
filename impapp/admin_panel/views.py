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
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
import traceback
from django.views.decorators.csrf import csrf_exempt



@login_required
def dashboard(request):
    return render_to_response('dashboard.html', {'request': request, 'menu': 'dashboard'},
                              context_instance=RequestContext(request))


@login_required
def all_users(request):
    try:
        query_string = request.GET.get('query_string')
        fields = request.GET.getlist('fields')
        print request
        argument_list = []
        if query_string and fields:
            for query in query_string.split(' '):
                for field in fields:
                    argument_list.append(Q(**{field+'__icontains': query}))

        all_user = User.objects.all()
        if query_string and fields:
            all_user = all_user.filter( reduce(operator.or_, argument_list))
            print all_user.query

        page_size = 20
        paginator = Paginator(all_user, page_size)
        page = request.GET.get('page')
        try:
            all_user = paginator.page(page)
        except PageNotAnInteger:
            all_user = paginator.page(1)
        except EmptyPage:
            all_user = paginator.page(paginator.num_pages)

        selection_fields = {'name': 'Name', 'id': 'Id', 'city': 'City', 'age': 'Age', 'email': 'Email',
                            'agent': 'Agent', 'profile_rating': 'Profile Rating', 'is_approved': 'Is Approved',
                            'is_public': 'Is Public', 'is_active': 'Is Active'}

        return render_to_response('all_users.html', {'request': request, 'menu': 'all_users', 'all_user': all_user,
                                                     'selection_fields': selection_fields, "page_size": page_size ,
                                                     "query_string": query_string,"fields": fields },
                                  context_instance=RequestContext(request))
    except Exception, ex:
        print traceback.print_exc(5)
        print str(ex)


@login_required
def update_all_ratings(request):
    update_rows = refresh_ratings()
    return render_to_response('refresh_ratings.html', {'request': request, 'menu': 'refresh_ratings',"update_rows": update_rows},
                              context_instance=RequestContext(request))

@login_required
def custom_attributes_list(request):
    attrib_list = CustomAttributes.objects.all()
    return render_to_response('custom_attributes.html', {'request': request, 'menu': 'custom_attributes',
                                                         "attrib_list":attrib_list},
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
        user_obj = User.objects.get(id=user_id)
        delete_images(user_obj)
        user_obj.delete()
        msg = "User has been delete successfully."
    except Exception,ex:
        print ex
        msg = str(ex)

    return HttpResponseRedirect(redirect_url+"?msg="+msg)


def del_ratings(request):
    try:
        redirect_url = request.GET["redirect_url"]
        user_id = request.GET["user_id"]
        user_obj = User.objects.get(id=user_id)
        ratings = Ratings.objects.filter(rated_profile=user_obj)
        ratings.delete()
        user_obj.profile_rating=None
        user_obj.save()
        msg = "User ratings have been delete successfully."
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
        is_active = 1 if is_active else 0

        is_public = request.POST.get('is_public')
        is_public = 1 if is_public else 0

        is_approved = request.POST.get('is_approved')
        is_approved = 1 if is_approved else 0

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


def add_edit_attribute(request):
    try:
        c_id = request.POST.get('c_id')
        key = request.POST['key']
        val = request.POST.get("val",'')
        desc = request.POST.get("desc",'')
        redirect_url = request.POST["redirect_url"]
        if c_id:
            attr = CustomAttributes.objects.filter(id=c_id)
            attr = attr[0] if attr else CustomAttributes()
            msg = "Custom Attribute Updated."
        else:
            attr = CustomAttributes()
            msg = "Custom Attribute Added."
        attr.desc = desc
        attr.key = key
        attr.val = val
        attr.save()

    except Exception, ex:
        print ex
        msg = str(ex)
    return HttpResponseRedirect(redirect_url+"?msg="+msg)


def del_attribute(request):
    try:
        redirect_url = request.GET["redirect_url"]
        cid = request.GET["c_id"]
        CustomAttributes.objects.get(id=cid).delete()
        msg = "Custom Attribute has been delete successfully."
    except Exception,ex:
        print ex
        msg = str(ex)

    return HttpResponseRedirect(redirect_url+"?msg="+msg)


def get_attrib(request):
    out_dict = {}
    try:
        cid = request.GET["c_id"]
        cus_obj = CustomAttributes.objects.get(id=cid)
        out_dict = make_cus_attr_dict(cus_obj)
    except Exception,ex:
        print ex
    return HttpResponse(json.dumps(out_dict))

def get_images(request):
    out_list = []
    try:
        user_id = request.GET['user_id']
        user_obj = User.objects.get(id=user_id)
        out_list = make_user_images(user_obj)

    except Exception,ex:
        import traceback
        print traceback.print_exc(5)
        print ex

    return HttpResponse(json.dumps(out_list))


@csrf_exempt
@login_required
def pending_users(request):
    try:
        msg = ''
        msg_type = ''
        if request.method=="POST":
            user_ids = request.POST.getlist('user_id')
            if not user_ids:
                msg = "No user has been selected"
            else:
                User.objects.filter(id__in=user_ids).update(is_approved=1)
                msg = "User(s) have been updated."
        all_users = User.objects.filter(is_approved=0).order_by('-created_on')
        return render_to_response('pending_users.html', {'request': request, 'menu': 'pending_users',
                                                             'all_users': all_users,"msg":msg,'msg_type': msg_type},
                                  context_instance=RequestContext(request))
    except:
        print traceback.print_exc(5)


