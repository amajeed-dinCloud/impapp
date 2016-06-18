__author__ = 'Abdul'
from django.conf.urls import url
from impapp.admin_panel.views import *
# from django.contrib import admin
urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^update_all_ratings', update_all_ratings),
    url(r'^custom_attributes_list', custom_attributes_list),
    url(r'^top_ten', top_ten),
    url(r'^del_user', del_user),
    url(r'^get_user', get_user),
    url(r'^update_user', update_user),



]
