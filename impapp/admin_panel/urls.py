__author__ = 'Abdul'
from django.conf.urls import url
from impapp.admin_panel.views import *
# from django.contrib import admin
urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^update_all_ratings', update_all_ratings),
    url(r'^custom_attributes_list', custom_attributes_list),
    url(r'^top_ten', top_ten),
    url(r'^contests', contests),
    url(r'^all_users', all_users),
    url(r'^pending_users', pending_users),
    url(r'^del_user', del_user),
    url(r'^del_ratings', del_ratings),
    url(r'^get_user', get_user),
    url(r'^update_user', update_user),
    url(r'^add_edit_attribute', add_edit_attribute),
    url(r'^del_attribute', del_attribute),
    url(r'^get_attrib', get_attrib),
    url(r'^get_images', get_images),
    url(r'^get_contest_users', get_contest_users),


]
