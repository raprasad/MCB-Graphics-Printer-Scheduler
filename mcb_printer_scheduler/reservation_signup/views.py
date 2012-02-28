from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from datetime import datetime, date, timedelta, time

from calendar_event.models import CalendarEvent, Reservation
from reservation_type.time_slot_maker import TimeSlotChecker
from reservation_signup.forms import SignupForm

from cal_util.view_util import get_common_lookup
from cal_util.msg_util import *

from django.core.urlresolvers import reverse

@login_required    #(login_url=reverse('view_current_month_calendar'))
def view_signup_page_success(request, id_hash):
    if id_hash is None:
        raise Http404('Reservation not found.')
    
    if not request.user.is_authenticated():
        lu.update({ 'ERR_found' : True, 'ERR_not_authenticated' : True })
        return render_to_response('reservation_signup/signup_success.html', lu, context_instance=RequestContext(request))
    
    try:
        reservation = CalendarEvent.objects.get(id_hash=id_hash, is_visible=True)
    except CalendarEvent.DoesNotExist:
        raise Http404('Reservation not found.')
    
    lu = get_common_lookup(request)
    lu.update({'reservation' : reservation
            , 'selected_date' : reservation.start_datetime.date() })
    
    timeslot_checker = TimeSlotChecker(selected_date=reservation.start_datetime.date())
    lu.update({ 'calendar_events' : timeslot_checker.calendar_events })
    
    return render_to_response('reservation_signup/signup_success.html', lu, context_instance=RequestContext(request))
        
        
    
#@login_required #(login_url=reverse('view_current_month_calendar'))
def view_signup_page(request, selected_date):
    if selected_date is None:
        raise Http404('Signup date not found.')

    lu = get_common_lookup(request)
    cal_user = lu.get('calendar_user', None)

    try:
        selected_datetime = datetime.strptime(selected_date, '%Y-%m-%d')
    except:
        return HttpResponse('Sign up date is not valid')
    
    selected_date = selected_datetime.date()
    lu.update({ 'selected_date' : selected_date})

    if not request.user.is_authenticated():
        lu.update({ 'ERR_found' : True, 'ERR_not_authenticated' : True })
        return render_to_response('reservation_signup/standard_signup_page.html', lu, context_instance=RequestContext(request))

    timeslot_checker = TimeSlotChecker(selected_date=selected_date)
    if timeslot_checker.err_found():
        lu.update({ 'ERR_found' : True })
        lu.update(timeslot_checker.get_lookup_for_template())
        return render_to_response('reservation_signup/standard_signup_page.html', lu, context_instance=RequestContext(request))
        
    lu.update(timeslot_checker.get_lookup_for_template())
    if request.method == 'POST': # If the form has been submitted...
        signup_form = SignupForm(request.POST) # A form bound to the POST data
        if signup_form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            new_signup = signup_form.get_reservation(lu.get('calendar_user'))
            
            success_url = reverse('view_signup_page_success'\
                            , kwargs={  'id_hash' : new_signup.id_hash }\
                            )
            return HttpResponseRedirect(success_url) # Redirect after POST
        else:
            signup_form.init(timeslot_checker.get_timeslot_choices_for_form()\
                            , timeslot_checker.get_reservation_time_block()
                            , cal_user )
    else:
        signup_form = SignupForm()
        signup_form.init(timeslot_checker.get_timeslot_choices_for_form()\
                        , timeslot_checker.get_reservation_time_block()
                        , cal_user)
            
    lu.update({ 'signup_form' : signup_form})
    
    return render_to_response('reservation_signup/standard_signup_page.html', lu, context_instance=RequestContext(request))
        
        
        
        
        
        
        
        
        
        
