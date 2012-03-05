# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from datetime import datetime, date, timedelta, time

from calendar_event.models import CalendarEvent, Reservation
from reservation_type.time_slot_maker import TimeSlotChecker
from admin_signup.form_blackout import AdminBlackoutForm

from cal_util.view_util import get_common_lookup
from cal_util.msg_util import *

from django.core.urlresolvers import reverse

@login_required 
def view_blackout_signup_page(request, selected_date):
    if selected_date is None:
        raise Http404('Signup date not found.')

    lu = get_common_lookup(request)

    cal_user = lu.get('calendar_user', None)
    if cal_user is None or not cal_user.is_calendar_admin:
        lu.update({ 'ERR_found' : True, 'ERR_no_permission_to_reserve_as_admin' : True })
        return render_to_response('admin_signup/blackout_signup_page.html', lu, context_instance=RequestContext(request))
        
    try:
        selected_datetime = datetime.strptime(selected_date, '%Y-%m-%d')
    except:
        return HttpResponse('Sign up date is not valid')
    
    selected_date = selected_datetime.date()
    lu.update({ 'selected_date' : selected_date})

    if not request.user.is_authenticated():
        lu.update({ 'ERR_found' : True, 'ERR_not_authenticated' : True })
        return render_to_response('admin_signup/blackout_signup_page.html', lu, context_instance=RequestContext(request))

    timeslot_checker = TimeSlotChecker(selected_date=selected_date)
    if timeslot_checker.err_found():
        lu.update({ 'ERR_found' : True })
        lu.update(timeslot_checker.get_lookup_for_template())
        return render_to_response('admin_signup/blackout_signup_page.html', lu, context_instance=RequestContext(request))
        
    lu.update(timeslot_checker.get_lookup_for_template())
    if request.method == 'POST': # If the form has been submitted...
        signup_form = AdminBlackoutForm(request.POST) # A form bound to the POST data
        if signup_form.is_valid(): # All validation rules pass
            new_signup = signup_form.get_calendar_event()
            
            success_url = reverse('view_admin_signup_page_success'\
                            , kwargs={  'id_hash' : new_signup.id_hash }\
                            )
            return HttpResponseRedirect(success_url) # Redirect after POST
        else:
            signup_form.init(timeslot_checker.get_timeslot_choices_for_form()\
                            , timeslot_checker.get_reservation_time_block()
                            , cal_user )
    else:
        signup_form = AdminBlackoutForm()
        signup_form.init(timeslot_checker.get_timeslot_choices_for_form()\
                        , timeslot_checker.get_reservation_time_block()
                        , cal_user)
            
    lu.update({ 'signup_form' : signup_form})
    
    return render_to_response('admin_signup/reservation_signup_page.html', lu, context_instance=RequestContext(request))
        
        
        
        
        
        
        
        
        
        
