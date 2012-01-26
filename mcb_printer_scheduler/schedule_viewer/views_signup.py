from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

from django.views.decorators.cache import never_cache


def view_signup_form(request):
    return HttpResponse('hello')
    # Create your views here.
