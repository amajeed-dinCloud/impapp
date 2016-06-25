__author__ = 'Abdul'
from impapp.app.models import *
from impapp import configs as conf
import traceback
import datetime

def update_profile_image_internal(user_obj, img_id):
    user_images = Document.objects.filter(user=user_obj)
    previous_image = user_images.filter(type=1)
    profile_images = user_images.filter(id=img_id)
    if profile_images:
        previous_image.update(type=2)
        profile_images.update(type=1)
        return True
    return False


def make_user_response(user_obj, hide_pass=None):
    user_dict = {"name": user_obj.name, "age": user_obj.age, "city": user_obj.city, "fb_id": user_obj.fb_id,
                 "profile_rating": user_obj.profile_rating, "is_public": True if user_obj.is_public else False, "email": user_obj.email,
                 "user_images": make_user_images(user_obj), "ins_id": user_obj.ins_id, "password": user_obj.password,
                 "id": user_obj.id, "is_active": True if user_obj.is_active else False,
                 "is_approved": True if user_obj.is_approved else False}

    if hide_pass:
        del(user_dict["password"])
    return user_dict


def make_user_images(user_obj):
    user_images = Document.objects.filter(user=user_obj).order_by('type')
    out_list = []
    for image in user_images:
        out_list.append(make_image_dict(image))
    return out_list


def make_image_dict(image):
    return {"img_url": conf.CURRENT_HOST+str(image.image.url), "type": image.type, "img_id": image.id}


def delete_images(user_obj, img_ids=None):
    if img_ids:
        images_to_delete = Document.objects.filter(user=user_obj, id__in=img_ids)
    else:
        images_to_delete = Document.objects.filter(user=user_obj)
    if images_to_delete:
        for img in images_to_delete:
            img.image.delete()
            img.delete()
        return True
    return False


def is_user_exists(email, fb_id, ins_id):
    user_obj = None
    if email:
        user_obj = User.objects.filter(email=email)
    if not user_obj and fb_id:
        user_obj = User.objects.filter(fb_id=fb_id)
    if not user_obj and ins_id:
        user_obj = User.objects.filter(ins_id=ins_id)

    if user_obj:
        user_obj = user_obj[0]

    return user_obj


def make_cus_attr_dict(cus_obj):
    out_dict = {"id": cus_obj.id, "val": cus_obj.val, "desc": cus_obj.desc, "key": cus_obj.key}
    return out_dict


def get_top_10_users():
    custom_attr = CustomAttributes.objects.filter(key='top_ten_min_votes')
    vote_limit = 1
    try:
        vote_limit = int(custom_attr[0].val) if custom_attr else 1
    except Exception,ex:
        print ex

    top_ten_users = User.objects.filter(is_approved=1, is_public=1, is_active=1, vote_count__gte=vote_limit
                                                ).order_by('-vote_count').order_by('-profile_rating')[:10]

    return top_ten_users


def get_contest_counter():
    contest_end_date = CustomAttributes.objects.filter(key='contest_ending_date')
    counter = {"days": 0, "hours": 0, "minutes": 0, "seconds": 0}
    try:
        if contest_end_date:
            contest_end_date = contest_end_date[0].val
            end_date = datetime.datetime.strptime(contest_end_date, '%m/%d/%Y  %I:%M %p')
            current_time = datetime.datetime.now()
            diff = end_date-current_time
            if diff.total_seconds() > 0:
                hours, remainder = divmod(diff.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                counter = {"days": diff.days, "hours": hours, "minutes": minutes, "seconds": seconds}
    except Exception,ex:
        print str(ex)
        print traceback.print_exc(5)
    return counter