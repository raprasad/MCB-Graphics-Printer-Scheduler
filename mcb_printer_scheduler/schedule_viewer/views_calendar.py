from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.cache import never_cache
from datetime import datetime

from calendar_event.models import CalendarEvent
from calendar_event.calendar_event_helper import CalendarEventOrganizer
from cal_util.view_util import get_common_lookup

def view_month_calendar(request, selected_year=None, month=selected_month):
    """
    View monthly calendar
    """
    lu = get_common_lookup(request)

    cal_user = lu.get('cal_user', None)

    current_datetime = datetime.now()
            
    if year is None or month is None:
        selected_year = current_datetime.year
        selected_month= current_datetime.month
    
    try:
        selected_month = datetime.datetime(year=selected_year, month=selected_month, day=1)
    except:
        selected_month = datetime.datetime(year=current_datetime.year, month=current_datetime.month, day=1)
        
    
    lu.update({'current_datetime':current_datetime\
                , 'selected_month' : selected_month })
    
        
    cal_events = CalendarEvent.objects.filter(is_visible=True)
    cal_events = cal_events.filter(Q(start_time__year=selected_month.year, start_time__month=selected_month.month)|\
                         Q(end_time__year=selected_month.year, end_time__month=selected_month.month)).order_by('start_time')
                                    
    cal_events = CalendarEventOrganizer.add_calendar_event_subclasses(cal_events)
    num_events = len(cal_events)
    lu.update( { 'cal_events' : cal_events\
                , 'num_events' : num_events })

    month_list = []
    for x in range(1,13):
        month_list.append(make_date_obj(start_date_selected.year, x, 1))
    
    
    lu.update( {'day_events_organizer' : day_events_organizer \
            , 'month_list' : month_list \
            , 'frequency' : freq
            ,'prev_year':start_date.year-1 \
            ,'next_year':start_date.year+1 \
            , 'category_list' : EventCategory.objects.all() \
           })
    lu.update(FREQ_LU)

    if template is None:
        if freq == VIEW_DAYS_DAILY: 
            template = 'calendar_event_html/day_calendar.html'
        else:
            template = 'calendar_event_html/month_calendar.html'
            
    return render_to_response(template, lu, context_instance=RequestContext(request))
    
    
