from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.cache import never_cache
from django.db.models import Q
from django.conf import settings

from datetime import datetime, date, timedelta

from calendar_event.models import CalendarEvent, ScheduledBannerMessage
from calendar_event.calendar_event_helper import CalendarEventOrganizer
from schedule_maker.day_events_organizer import DayEventsOrganizer
from schedule_maker.calendar_weeks import get_calendar_weeks


from cal_util.view_util import get_common_lookup
from cal_util.time_util import get_next_month, get_previous_month

from cal_util.msg_util import *

def view_month_calendar(request, selected_month=None):
    """
    View monthly calendar
    """
    current_datetime = datetime.now()
    if selected_month is None:
        selected_month = current_datetime.date()
        is_current_month = True
    else:
        try:
            selected_month = datetime.strptime(selected_month, '%Y-%m')
        except:
            raise ValueError('selected month is not valid')
        
        if current_datetime.month == selected_month.month \
            and current_datetime.year ==  selected_month.year:
            is_current_month = True
        else:
            is_current_month = False
    
    lu = get_common_lookup(request)
    
    lu.update({'current_datetime':current_datetime\
                , 'is_current_month' : is_current_month
                , 'selected_month' : selected_month
                , 'HU_PIN_LOGIN_APP_NAME' : settings.HU_PIN_LOGIN_APP_NAME })
    
    
    # Create a list of the weeks. Each week is a list of seven datetime.date objects.
    cal_weeks = get_calendar_weeks(selected_month)  

    # query for calendar events in selected months, including days in week from prev/next month
    cal_events = CalendarEvent.objects.filter(is_visible=True)
    #print 'start day', cal_weeks[0][0]
    #print 'end day', cal_weeks[-1][-1]
    filter_start_day = datetime(cal_weeks[0][0].year, cal_weeks[0][0].month, cal_weeks[0][0].day)
    filter_end_day = datetime(cal_weeks[-1][-1].year, cal_weeks[-1][-1].month, cal_weeks[-1][-1].day) + timedelta(days=1, microseconds=-1)
    
    # everything where the *start* time falls within the filter boundaries
    cal_events = cal_events.filter(start_datetime__gte=filter_start_day\
                                 , start_datetime__lte=filter_end_day).order_by('start_datetime')

    #cal_events = cal_events.filter(Q(start_datetime__gte=filter_start_day\
    #                                ,start_datetime__lte=filter_end_day) | \
    #                            ).order_by('start_datetime')
    
                                    
    cal_events = CalendarEventOrganizer.substitute_cal_event_subclasses(cal_events)
    
    num_events = len(cal_events)
    
    day_events_organizer = DayEventsOrganizer(cal_weeks, cal_events)

    lu.update( { 'day_events_organizer' : day_events_organizer \
                ,'cal_events' : cal_events\
                , 'num_events' : num_events })

    month_list = []
    for x in range(1,13):
        month_list.append(date(selected_month.year, x, 1))
    
    
    lu.update( {'month_list' : month_list \
            ,'prev_year':selected_month.year-1 \
            ,'next_year':selected_month.year+1 \
            , 'next_month' : get_next_month(selected_month)
            , 'previous_month' :  get_previous_month(selected_month)
            , 'banner_messages' : ScheduledBannerMessage.objects.filter(is_active=True\
                                    , start_datetime__lte=current_datetime\
                                    , end_datetime__gte=current_datetime).all()
           })

    template = 'schedule_viewer/month_calendar.html'
            
    return render_to_response(template, lu, context_instance=RequestContext(request))
    
    
