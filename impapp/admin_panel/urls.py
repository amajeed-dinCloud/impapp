__author__ = 'Abdul'
from django.conf.urls import url
from impapp.admin_panel.views import *
# from django.contrib import admin
urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^update_all_ratings', update_all_ratings),
    url(r'^custom_attributes_list', custom_attributes_list),



]
