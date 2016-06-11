__author__ = 'Abdul'
from impapp.app.models import *
from impapp import configs as conf


def update_profile_image_internal(user_obj, img_id):
    user_images = Document.objects.filter(user=user_obj)
    previous_image = user_images.filter(type=1)
    profile_images = user_images.filter(id=img_id)
    if profile_images:
        previous_image.update(type=2)
        profile_images.update(type=1)
        return True
    return False


def make_user_response(user_obj):
    return {"name": user_obj.name, "age": user_obj.age, "city": user_obj.city, "fb_id": user_obj.fb_id,
            "profile_rating": user_obj.profile_rating, "is_public": user_obj.is_public, "email": user_obj.email,
            "user_images": make_user_images(user_obj), "ins_id": user_obj.ins_id, "password": user_obj.password,
            "is_public": user_obj.is_public, "id": user_obj.id}


def make_user_images(user_obj):
    user_images = Document.objects.filter(user=user_obj)
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
