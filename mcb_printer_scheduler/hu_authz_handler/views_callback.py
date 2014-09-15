from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail

from calendar_user.models import CalendarUser
#from cal_util.view_util import get_common_lookup

#from hu_pin_auth.pin_login_handler import PinLoginHandler
#from hu_authzproxy.authzproxy_login_handler import AuthZProxyLoginHandler
#from hu_authzproxy.authz_proxy_validation_info import AuthZProxyValidationInfo

from django.conf import settings

"""def view_logout_page(request):

    lu = get_common_lookup(request)

    cal_user = lu.get('calendar_user', None)
    
    if not request.user.is_authenticated():
        lu.update({ 'ERR_found' : True, 'ERR_already_logged_out' : True })
        return render_to_response('login/logout_page.html', lu, context_instance=RequestContext(request))
"""

def get_or_create_calendar_user(django_user):
    try:
        cal_user = CalendarUser.objects.get(user=django_user)
    except CalendarUser.DoesNotExist:
        cal_user = CalendarUser(user=django_user #pin_login_handler.get_user()\
                        , is_calendar_admin=False
                        )
        if django_user.email:
            cal_user.contact_email=django_user.email
        else:
            cal_user.contact = 'need_email@harvard.edu'
        cal_user.save()

    return cal_user
    
def view_handle_authz_callback(request):
    """View to handle pin callback
    If authentication is succesful:
        - go to a specified 'next' link 
        - or default to the django admin index page
    """
    #print 'blah'
    if request.user.is_authenticated():
        # make sure still exists (e.g. CalendarUser not deleted during session)
        if request.user.calendaruser_set.count() == 0:  # deleted, log the user out
            logout(request)
        else:
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


    authz_validation_info = AuthZProxyValidationInfo(request=request\
                                  ,app_names=settings.HU_PIN_LOGIN_APP_NAMES\
                                  , gnupghome=settings.GNUPG_HOME 
                                  , gpg_passphrase=settings.GPG_PASSPHRASE
                                  , is_debug=settings.DEBUG)

    authz_pin_login_handler = AuthZProxyLoginHandler(authz_validation_info\
                                      , **access_settings)


    if authz_pin_login_handler.did_login_succeed():
        django_user = authz_pin_login_handler.get_user()
        login(request, django_user)
        
        get_or_create_calendar_user(django_user)
        """
        try:
            cal_user = CalendarUser.objects.get(user=django_user)
        except CalendarUser.DoesNotExist:
            cal_user = CalendarUser(user=django_user #pin_login_handler.get_user()\
                            , is_calendar_admin=False
                            , contact_email=django_user.email)
            cal_user.save()
        """
        return HttpResponseRedirect(next)

    # Errors while logging in!
    # 
    # Retrieve error messages from the AuthZProxyLoginHandler
    error_messages = []
    authz_errs = authz_pin_login_handler.get_err_msgs()
    if not authz_errs is None:
        error_messages += authz_errs

    # Retrieve error flags from the AuthZProxyLoginHandler
    err_dict = authz_pin_login_handler.get_error_dict()   # get error lookup for use 
    for k,v in err_dict.iteritems():
        if v is True:
            error_messages.append(' %s -> [%s]' % (k,v))

    # add the user IP address
    error_messages.append('user IP address: %s' % request.META.get('REMOTE_ADDR', None))


    # send email message to the admins
    try:
        admin_emails = map(lambda x: x[1], settings.ADMINS)
    except:
        admin_emails = None
    print admin_emails
    if admin_emails and len(admin_emails) > 0:
        send_mail('mcb printer scheduler db log in fail info', 'Here is the message. %s' % ('\n'.join(error_messages)), admin_emails[0], admin_emails,fail_silently=False)

    # send the error flags to the template
    return render_to_response('hu_authz_handler/view_authz_login_failed.html', err_dict, context_instance=RequestContext(request))
    
    # return render_to_response('login/login_failed.html', err_dict, context_instance=RequestContext(request))

