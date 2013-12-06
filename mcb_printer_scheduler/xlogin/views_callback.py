from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from hu_pin_auth.pin_login_handler import PinLoginHandler

from calendar_user.models import CalendarUser
from cal_util.view_util import get_common_lookup


def view_logout_page(request):

    lu = get_common_lookup(request)

    cal_user = lu.get('calendar_user', None)
    
    if not request.user.is_authenticated():
        lu.update({ 'ERR_found' : True, 'ERR_already_logged_out' : True })
        return render_to_response('login/logout_page.html', lu, context_instance=RequestContext(request))




def view_handle_pin_callback(request):
    """View to handle pin callback
    If authentication is succesful:
        - go to a specified 'next' link 
        - or default to the django admin index page
    """
    if request.user.is_authenticated():
        print '(1) already authenticated'
        return HttpResponseRedirect(reverse('view_current_month_calendar', kwargs={}))

    #
    if request.GET and request.GET.get('next', None) is not None:
        next = request.GET.get('next')
    else:
        next =  reverse('view_current_month_calendar', kwargs={})
    print '(2) next: %s' % next
        
    # How Django handles authentication after pin is verfied. 
    # See "pin_login_handler.PinLoginHandler" class handler for more info
    #
    # This ALLOWS ANYONE WITH A HARVARD PIN To log in
    access_settings = { 'restrict_to_existing_users':False \
                         , 'restrict_to_active_users':False \
                         , 'restrict_to_staff':False \
                         , 'restrict_to_superusers':False}

    pin_login_handler = PinLoginHandler(request, **access_settings)    # request object
    if pin_login_handler.did_login_succeed():
        print '(3) login success'
        django_user = pin_login_handler.get_user()
        
        login(request, django_user)
        
        try:
            cal_user = CalendarUser.objects.get(user=django_user)
        except CalendarUser.DoesNotExist:
            cal_user = CalendarUser(user=pin_login_handler.get_user()\
                        , is_calendar_admin=False
                        , contact_email=django_user.email)
            cal_user.save()
     
        return HttpResponseRedirect(next)
    else:
        print '(4) login failed'
        err_dict = pin_login_handler.get_error_dict()   # get error lookup for use in template
        print '-' * 20
        for k,v in err_dict.iteritems():
            print ' %s -> [%s]' % (k,v)
        return render_to_response('login/login_failed.html', err_dict, context_instance=RequestContext(request))

