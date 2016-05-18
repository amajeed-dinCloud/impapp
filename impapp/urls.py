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
from django.conf.urls import url,include
from django.conf.urls.static import static
import settings
from impapp.app.views import isworking, redirect_insta
# from django.contrib import admin

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^service/',include('impapp.app.urls')),
    url(r'^$', isworking),
    url(r'^redirect_insta',redirect_insta),

    # static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
