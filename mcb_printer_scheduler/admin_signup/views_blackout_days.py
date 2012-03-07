# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from datetime import datetime, date, timedelta, time

from calendar_event.models import CalendarEvent, CalendarFullDayMessage
from reservation_type.time_slot_maker import TimeSlotChecker
from admin_signup.forms_blackout import AdminBlackoutDaysForm

from django.utils import simplejson
from cal_util.ajax_util import render_to_string_remove_spaces, get_json_str_as_http_response2

from cal_util.view_util import get_common_lookup
from cal_util.msg_util import *

from django.core.urlresolvers import reverse


@login_required 
def view_blackout_days_signup_page(request, selected_date):
    if selected_date is None:
        raise Http404('Signup date not found.')

    lu = get_common_lookup(request)
    lu.update({ 'admin_blackout_days' : True })

    cal_user = lu.get('calendar_user', None)
    if cal_user is None or not cal_user.is_calendar_admin:
        lu.update({ 'ERR_found' : True, 'ERR_no_permission_to_reserve_as_admin' : True })
        return render_to_response('admin_signup/blackout_days_signup_page.html', lu, context_instance=RequestContext(request))
        
    try:
        selected_datetime = datetime.strptime(selected_date, '%Y-%m-%d')
    except:
        return HttpResponse('Sign up date is not valid')
    
    selected_date = selected_datetime.date()
    lu.update({ 'selected_date' : selected_date})

    timeslot_checker = TimeSlotChecker(selected_date=selected_date)
    if timeslot_checker.err_found():
        lu.update({ 'ERR_found' : True })
        lu.update(timeslot_checker.get_lookup_for_template())
        return render_to_response('admin_signup/blackout_days_signup_page.html', lu, context_instance=RequestContext(request))
        
    lu.update(timeslot_checker.get_lookup_for_template())
    if request.method == 'POST': # If the form has been submitted...
        signup_form = AdminBlackoutDaysForm(request.POST) # A form bound to the POST data
        if signup_form.is_valid(): # All validation rules pass
            new_signup = signup_form.get_calendar_event()
            print 'new_signup', new_signup
            success_url = reverse('view_blackout_signup_success'\
                            , kwargs={  'id_hash' : new_signup.id_hash }\
                            )
            return HttpResponseRedirect(success_url) # Redirect after POST
        else:
            signup_form.init(selected_date)
    else:
        signup_form = AdminBlackoutDaysForm()
        signup_form.init(selected_date)
            
    lu.update({ 'signup_form' : signup_form})
    
    return render_to_response('admin_signup/blackout_days_signup_page.html', lu, context_instance=RequestContext(request))
     