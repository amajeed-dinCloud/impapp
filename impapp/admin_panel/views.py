__author__ = 'Abdul'
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from impapp.update_ratings import refresh_ratings
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.template.loader import get_template

@login_required
def is_working(request):
    return render_to_response('dashboard.html', {'request': request, 'menu': 'dashboard'},
                              context_instance=RequestContext(request))
    # return HttpResponse("*IS WORKING*")


@login_required
def update_all_ratings(request):
    update_rows = refresh_ratings()
    return HttpResponse("No of Row(s) updated: "+str(update_rows))

@login_required
def custom_attributes_list(request):
    return render_to_response('custom_attributes.html', {'request': request, 'menu': 'custom_attributes'},
                              context_instance=RequestContext(request))