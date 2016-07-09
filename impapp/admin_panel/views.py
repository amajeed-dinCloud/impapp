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
from impapp.app import functions as app_func
from django.db import connection
from django.db.models import Count
import csv



@login_required
def dashboard(request, msg=''):
    print msg
    active_users = User.objects.filter(is_active=1).count()
    pending_users = User.objects.filter(is_approved=0).count()
    total_users = User.objects.count()
    g_data = get_graph_data()
    info_dict = {"active_users":active_users, "pending_users": pending_users, "total_users": total_users}

    return render_to_response('dashboard.html', {'request': request, 'menu': 'dashboard', 'info_dict': info_dict,"msg":msg,
                                                 'g_data':g_data}, context_instance=RequestContext(request))


@login_required
def all_users(request):
    try:
        query_str = ''
        parmas = request.get_full_path().split(request.path+'?')
        if len(parmas) > 1:
            query_str = parmas[1]

        page_size = 20
        all_user = User.objects.all()
        email = request.GET.get('email')
        name = request.GET.get('name')
        city = request.GET.get('city')
        age = request.GET.get('age')
        rating = request.GET.get('rating')
        agent = request.GET.get('agent')
        is_active = request.GET.get('is_active')
        is_public = request.GET.get('is_public')
        is_approved = request.GET.get('is_approved')
        submit = request.GET.get('submit')
        page = request.GET.get('page')

        if email:
            all_user = all_user.filter(email__icontains=email)
        if name:
            all_user = all_user.filter(name__icontains=name)
        if city:
            all_user = all_user.filter(city__icontains=city)
        if age:
            all_user = all_user.filter(age=age)
        if rating:
            all_user = all_user.filter(profile_rating__icontains=rating)
        if agent:
            all_user = all_user.filter(agent__icontains=agent)
        if is_active == '1':
            all_user = all_user.filter(is_active=1)
        elif is_active == '0':
            all_user = all_user.filter(is_active=0)

        if is_public == '1':
            all_user = all_user.filter(is_public=1)
        elif is_public == '0':
            all_user = all_user.filter(is_public=0)

        if is_approved == '1':
            all_user = all_user.filter(is_approved=1)
        elif is_approved == '0':
            all_user = all_user.filter(is_approved=0)

        if submit == "download_report":
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="user_info.csv"'
            writer = csv.writer(response)

            if all_user:
                header = ['Name', 'City', 'Age', 'Email', 'Rating', 'IS Approved', 'Is Public', 'Is Active',
                          'User Agent', 'Vote Count', "Created On", "Updated On"]
                writer.writerow(header)
                for u in all_user:
                    user_tuple = (u.name, u.city, u.age, u.email, u.profile_rating, u.is_approved, u.is_public,
                                  u.is_active, u.agent, u.vote_count,u.created_on, u.updated_on)
                    writer.writerow(user_tuple)
                return response


        paginator = Paginator(all_user, page_size)

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
                                                     'selection_fields': selection_fields, "page_size": page_size,
                                                     "query_str": query_str},
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
    attrib_list = CustomAttributes.objects.all().exclude(key='contest_ending_date').order_by('-updated_on')
    return render_to_response('custom_attributes.html', {'request': request, 'menu': 'custom_attributes',
                                                         "attrib_list":attrib_list},
                              context_instance=RequestContext(request))

@login_required
def top_ten(request):
    top_ten_users = get_top_10_users()
    return render_to_response('top_ten.html', {'request': request, 'menu': 'top_ten',
                                                         'top_ten_users': top_ten_users},
                              context_instance=RequestContext(request))


def contests(request):
    try:
        if request.method == 'POST':
            contest_end_date = request.POST.get('contest_ending_date')
            if contest_end_date:
                ca_end_date = CustomAttributes.objects.filter(key='contest_ending_date')
                if ca_end_date:
                    ca_end_date[0].val = contest_end_date
                    ca_end_date[0].save()
                else:
                    desc ="contest will be end on this date and ratings will be marked zero"
                    CustomAttributes.objects.create(desc=desc,key='contest_ending_date',val=contest_end_date)

        counter = app_func.get_contest_counter()
        contest_list = Contests.objects.all()

        return render_to_response('contests.html', {'request': request, 'menu': 'contests', 'counter':counter,
                                                    'contest_list': contest_list},
                                  context_instance=RequestContext(request))
    except Exception,ex:
        print str(ex)
        print traceback.print_exc(5)


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
        profile_rating = request.POST.get('profile_rating')

        is_active = request.POST.get('is_active')
        is_active = 1 if is_active else 0

        is_public = request.POST.get('is_public')
        is_public = 1 if is_public else 0

        is_approved = request.POST.get('is_approved')
        is_approved = 1 if is_approved else 0

        user_obj = User.objects.get(id=user_id)

        if profile_rating and profile_rating != user_obj.profile_rating:
            if util_functions.validate_float(profile_rating):
                user_obj.profile_rating = profile_rating
                Ratings.objects.filter(rated_profile=user_obj).update(rating=profile_rating)

        user_obj.name = name
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
        if request.method == "POST":
            user_ids = request.POST.getlist('user_id')
            if not user_ids:
                msg = "No user has been selected"
            else:
                User.objects.filter(id__in=user_ids).update(is_approved=1)
                msg = "User(s) have been updated."

        email = request.GET.get('email')
        name = request.GET.get('name')
        city = request.GET.get('city')
        age = request.GET.get('age')
        rating = request.GET.get('rating')
        agent = request.GET.get('agent')
        is_active = request.GET.get('is_active')
        is_public = request.GET.get('is_public')
        is_approved = request.GET.get('is_approved')
        submit = request.GET.get('submit')


        all_user = User.objects.filter(is_approved=0).order_by('-created_on')
        if email:
            all_user = all_user.filter(email__icontains=email)
        if name:
            all_user = all_user.filter(name__icontains=name)
        if city:
            all_user = all_user.filter(city__icontains=city)
        if age:
            all_user = all_user.filter(age=age)
        if rating:
            all_user = all_user.filter(profile_rating__icontains=rating)
        if agent:
            all_user = all_user.filter(agent__icontains=agent)
        if is_active == '1':
            all_user = all_user.filter(is_active=1)
        elif is_active == '0':
            all_user = all_user.filter(is_active=0)

        if is_public == '1':
            all_user = all_user.filter(is_public=1)
        elif is_public == '0':
            all_user = all_user.filter(is_public=0)

        if is_approved == '1':
            all_user = all_user.filter(is_approved=1)
        elif is_approved == '0':
            all_user = all_user.filter(is_approved=0)

        if submit == "download_report":
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="pending_users_info.csv"'
            writer = csv.writer(response)

            if all_user:
                header = ['Name', 'City', 'Age', 'Email', 'Rating', 'IS Approved', 'Is Public', 'Is Active',
                          'User Agent', 'Vote Count', "Created On", "Updated On"]
                writer.writerow(header)
                for u in all_user:
                    user_tuple = (u.name, u.city, u.age, u.email, u.profile_rating, u.is_approved, u.is_public,
                                  u.is_active, u.agent, u.vote_count,u.created_on, u.updated_on)
                    writer.writerow(user_tuple)
                return response


        return render_to_response('pending_users.html', {'request': request, 'menu': 'pending_users',
                                                             'all_users': all_user,"msg":msg,'msg_type': msg_type},
                                  context_instance=RequestContext(request))
    except:
        print traceback.print_exc(5)


def get_graph_data():
    keyword = 'day'
    truncate_date = connection.ops.date_trunc_sql(keyword, 'created_on')
    qs = User.objects.extra({keyword:truncate_date})
    all_users = qs.values(keyword).annotate(Count('pk')).order_by(keyword)[:30]
    android_users = qs.filter(agent='android').values(keyword).annotate(Count('pk')).order_by(keyword)[:30]
    ios_users = qs.exclude(agent='android').values(keyword).annotate(Count('pk')).order_by(keyword)[:30]
    data_set = []
    for data in all_users:
        inner_dict = {'count':data['pk__count'], keyword: str(data[keyword].strftime('%B %d, %y'))}
        for and_user in android_users:
            if data[keyword] == and_user[keyword]:
                inner_dict['and_user'] = and_user['pk__count']
                break
        for iso_user in ios_users:
            if data[keyword] == iso_user[keyword]:
                inner_dict['ios_user'] = iso_user['pk__count']
                break
        if not inner_dict.get('ios_user'):
            inner_dict['ios_user'] = 0
        if not inner_dict.get('and_user'):
            inner_dict['and_user'] = 0

        data_set.append(inner_dict)
    return data_set


def get_contest_users(request):
    out_str = ''
    try:
        contest_id = request.GET.get("contest_id")
        cong_obj = Contests.objects.get(pk=contest_id)
        contest_users = json.loads(cong_obj.top_ten)
        top_ten_users = []
        for u in contest_users:
                try:
                    user_obj=User.objects.get(id=u[0])
                    user_obj.profile_rating = u[1]
                    user_obj.vote_count = u[2]
                    top_ten_users.append(user_obj)
                except Exception,ex:
                    print ex
        if top_ten_users:
            out_str = '<table class="table table-striped table-bordered table-hover"><tr><th>Name</th>' \
                      '<th>Email</th><th>Age</th><th>City</th><th>Rating</th><th>Agent</th></tr></table>'
            for u in top_ten_users:
                email = '' if not u.email else u.email
                out_str=out_str.replace('</table>', '<tr><td>'+str(u.name)+'</td><td>'+str(email)+'</td><td>'+str(u.age)
                                        +'</td><td>'+str(u.city)+'</td><td>'+str(u.profile_rating)+'</td><td>'+str(u.agent)+'</td></tr></table>')

        else:
            out_str = "<h4>No user has been found in this contest.<h4>"

    except Exception, ex:
        print traceback.print_exc(5)
        out_str=str(ex)

    return HttpResponse(out_str)