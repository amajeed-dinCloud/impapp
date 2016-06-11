__author__ = 'Abdul'
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from impapp.update_ratings import refresh_ratings

@login_required
def is_working(request):
    return HttpResponse("*IS WORKING*")


@login_required
def update_all_ratings(request):
    update_rows = refresh_ratings()
    return HttpResponse("No of Row(s) updated: "+str(update_rows))