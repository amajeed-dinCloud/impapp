"""impapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from impapp.app.views import *
urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^sign_up', sign_up),
    url(r'^login', login),
    url(r'^update_profile', update_profile),
    url(r'^upload_image', upload_image),
    url(r'^update_profile_image', update_profile_image),
    url(r'^delete_user_image', delete_user_image),
    url(r'^get_users', get_users),
    url(r'^rate_user', rate_user),
    url(r'^delete_user', delete_user),
    url(r'^profiles_list', profiles_list),
    url(r'^update_user_image', update_user_image),
    url(r'^top_ten', top_ten),
    url(r'^get_custom_attributes', get_custom_attributes),
    url(r'^forgot_password', forgot_password),



]
# from django.contrib import admin

