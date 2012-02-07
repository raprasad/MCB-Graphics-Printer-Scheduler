from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.cache import never_cache
from django.db.models import Q

from datetime import datetime, date, timedelta, time

from calendar_event.models import CalendarEvent
#from calendar_event.calendar_event_helper import CalendarEventOrganizer
#from schedule_maker.day_events_organizer import DayEventsOrganizer
#from schedule_maker.calendar_weeks import get_calendar_weeks
from reservation_type.time_slot_maker import TimeSlotChecker

from cal_util.view_util import get_common_lookup
from cal_util.msg_util import *

def view_signup_page(request, selected_date):
    if selected_date is None:
        raise Http404('Signup date not found.')

    try:
        selected_datetime = datetime.strptime(selected_date, '%Y-%m-%d')
    except:
        return HttpResponse('Sign up date is not valid')
    
    selected_date = selected_datetime.date()
    
    lu = get_common_lookup(request)

    timeslot_checker = TimeSlotChecker(selected_date=selected_date)
    if timeslot_checker.err_found():
        lu.update({ 'ERR_found' : True })
        lu.update(timeslot_checker.get_lookup_for_template())
        return render_to_response('reservation_signup/standard_signup_page.html', lu, context_instance=RequestContext(request))
        
    lu.update(timeslot_checker.get_lookup_for_template())

    return render_to_response('reservation_signup/standard_signup_page.html', lu, context_instance=RequestContext(request))
        
        
        
        
        
        
        
        
        
        
