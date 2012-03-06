# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from datetime import datetime, date, timedelta, time

from calendar_event.models import CalendarEvent, CalendarMessage
from reservation_type.time_slot_maker import TimeSlotChecker
from admin_signup.form_blackout import AdminBlackoutForm

from django.utils import simplejson
from cal_util.ajax_util import render_to_string_remove_spaces, get_json_str_as_http_response2

from cal_util.view_util import get_common_lookup
from cal_util.msg_util import *

from django.core.urlresolvers import reverse


@login_required 
def get_valid_end_times(request, selected_date, selected_time=None):
    """Given a start_datetime, return an ajax list of end times"""
    if selected_date is None:
        return get_json_str_as_http_response2(request, False, "The start date was not found")
            
    if selected_time is None:
        return get_json_str_as_http_response2(request, False, "The start time was not found")
        
    try:
        time_str = '%s %s' % (selected_date, selected_time)
        selected_datetime = datetime.strptime(time_str, '%Y-%m-%d %H-%M')
    except:
        return get_json_str_as_http_response2(request, False, "The start time was not valid")
        

    timeslot_checker = TimeSlotChecker(selected_date=selected_datetime.date())
    end_time_options = timeslot_checker.get_end_times_for_ajax_call(selected_datetime)
    if end_time_options is None:
        return get_json_str_as_http_response2(request, False, "Sorry!  No end times are available")
    
    options_html = render_to_string_remove_spaces('admin_signup/ajax_end_time_options.html'\
                                , { 'end_time_options' : end_time_options})
    options_html_json = simplejson.dumps(options_html)
    
    return get_json_str_as_http_response2(request, True, msg=''\
                                , json_str=',"options_html" : %s' % options_html_json)



@login_required 
def view_blackout_signup_page(request, selected_date):
    if selected_date is None:
        raise Http404('Signup date not found.')

    lu = get_common_lookup(request)
    lu.update({ 'admin_blackout' : True })

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
            
            success_url = reverse('view_blackout_signup_success'\
                            , kwargs={  'id_hash' : new_signup.id_hash }\
                            )
            return HttpResponseRedirect(success_url) # Redirect after POST
        else:
            signup_form.init(timeslot_checker.get_start_time_choices_for_form()\
                            , timeslot_checker.get_end_time_choices_for_form() )
    else:
        signup_form = AdminBlackoutForm()
        signup_form.init(timeslot_checker.get_start_time_choices_for_form()\
                        , timeslot_checker.get_end_time_choices_for_form() )
            
    lu.update({ 'signup_form' : signup_form})
    
    return render_to_response('admin_signup/blackout_signup_page.html', lu, context_instance=RequestContext(request))
        
        
@login_required
def view_blackout_signup_success(request, id_hash):
    if id_hash is None:
        raise Http404('CalendarMessage not found.')

    lu = get_common_lookup(request)
    lu.update({ 'admin_blackout' : True })

    if not request.user.is_authenticated():
        lu.update({ 'ERR_found' : True, 'ERR_not_authenticated' : True })
        return render_to_response('admin_signup/blackout_signup_page_success.html', lu, context_instance=RequestContext(request))

    cal_user = lu.get('calendar_user', None)
    if cal_user is None or not cal_user.is_calendar_admin:
        lu.update({ 'ERR_found' : True, 'ERR_no_permission_to_reserve_as_admin' : True })
        return render_to_response('admin_signup/blackout_signup_page_success.html', lu, context_instance=RequestContext(request))

    try:
        calendar_message = CalendarEvent.objects.get(id_hash=id_hash, is_visible=True)
    except CalendarEvent.DoesNotExist:
        raise Http404('CalendarMessage not found.')

    lu.update({'calendar_message' : calendar_message
           , 'selected_date' : calendar_message.start_datetime.date() })

    timeslot_checker = TimeSlotChecker(selected_date=calendar_message.start_datetime.date())
    lu.update({ 'calendar_events' : timeslot_checker.calendar_events })

    return render_to_response('admin_signup/blackout_signup_page_success.html', lu, context_instance=RequestContext(request))







