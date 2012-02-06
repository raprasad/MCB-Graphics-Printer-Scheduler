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


from cal_util.view_util import get_common_lookup
from cal_util.msg_util import *

def view_signup_page(request, selected_date):
    if selected_date is None:
        raise Http404('Signup date not found.')


    try:
        selected_datetime = datetime.strptime(selected_date, '%Y-%m-%d')
    except:
        return HttpResponse('Sign up date is not valid')
    
    lu = get_common_lookup(request)

    # List the evetns for the selected day
    day_cal_events = CalendarEvent.objects.filter(is_visible=True\
                                 , start_time__gte=selected_datetime\
                                 , start_time__lte=datetime.combine(selected_datetime.date()\
                                 , time.max)).order_by('start_time')
                                 
    current_datetime = datetime.now()

    lu.update({'day_cal_events' : day_cal_events\
            , 'current_datetime' : current_datetime })

    cal_user = lu.get('cal_user', None)
    
    # has this day already passed
    if selected_datetime.date() < current_datetime.date():
        return render_to_response('reservation_signup/standard_signup_page.html', lu, context_instance=RequestContext(request))


    return render_to_response('reservation_signup/standard_signup_page.html', lu, context_instance=RequestContext(request))
        
        
        
        
        
        
        
        
        
        
