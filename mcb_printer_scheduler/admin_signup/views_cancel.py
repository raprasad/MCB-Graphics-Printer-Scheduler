import datetime

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from calendar_event.models import CalendarEvent, CalendarMessage
from reservation_type.time_slot_maker import TimeSlotChecker
from admin_signup.forms_cancel import CalendarEventCancellationForm

from cal_util.view_util import get_common_lookup
from cal_util.msg_util import *

from django.core.urlresolvers import reverse

@login_required
def view_cancel_calendar_message_success(request, id_hash, selected_date):
    if id_hash is None or selected_date is None:
        raise Http404('id_hash or date not found.')

    lu = get_common_lookup(request)

    try:
        selected_date = datetime.datetime.strptime(selected_date, '%Y-%m-%d').date()
        lu.update({'selected_date' : selected_date })
    except:
        raise Http404('selected_date date not found.')
    
    lu.update({ 'admin_blackout_cancel' : True })

    if not request.user.is_authenticated():
        lu.update({ 'ERR_found' : True, 'ERR_not_authenticated' : True })
        return render_to_response('admin_cancel/cancel_signup_success.html', lu, context_instance=RequestContext(request))

    cal_user = lu.get('calendar_user', None)
    if not cal_user.is_calendar_admin:
        lu.update({ 'ERR_found' : True, 'ERR_no_permission_to_cancel' : True })
        return render_to_response('admin_cancel/cancel_signup_success.html', lu, context_instance=RequestContext(request))


    if CalendarEvent.objects.filter(id_hash=id_hash).count() > 0:
        lu.update({ 'ERR_found' : True, 'ERR_calendar_event_not_cancelled' : True })
        return render_to_response('admin_cancel/cancel_signup_success.html', lu, context_instance=RequestContext(request))

        

    timeslot_checker = TimeSlotChecker(selected_date=selected_date)
    lu.update({ 'calendar_events' : timeslot_checker.calendar_events })

    lu.update({ 'cancel_success' : True })
    return render_to_response('admin_cancel/cancel_signup_success.html', lu, context_instance=RequestContext(request))
    
    
@login_required    
def view_cancel_calendar_message(request, id_hash):
    if id_hash is None:
        raise Http404('Reservation not found.')
    
    if not request.user.is_authenticated():
        lu.update({ 'ERR_found' : True, 'ERR_not_authenticated' : True })
        return render_to_response('admin_cancel/cancel_signup.html', lu, context_instance=RequestContext(request))
    
    try:
        calendar_message = CalendarEvent.objects.get(id_hash=id_hash, is_visible=True)
    except CalendarEvent.DoesNotExist:
        raise Http404('CalendarEvent not found.')
    
    lu = get_common_lookup(request)
    cal_user = lu.get('calendar_user', None)
    
    if not cal_user.is_calendar_admin:
        lu.update({ 'ERR_found' : True, 'ERR_no_permission_to_cancel' : True })
        return render_to_response('admin_cancel/cancel_signup.html', lu, context_instance=RequestContext(request))

    selected_date = calendar_message.start_datetime.date()

    lu.update({'calendar_message' : calendar_message
            , 'selected_date' : selected_date
            , 'admin_blackout_cancel' : True  })
    
    timeslot_checker = TimeSlotChecker(selected_date=selected_date)
    lu.update({ 'calendar_events' : timeslot_checker.calendar_events })


    if request.method == 'POST': # If the form has been submitted...
        cancel_form = CalendarEventCancellationForm(request.POST) # A form bound to the POST data
        if cancel_form.is_valid(): # All validation rules pass
            res = cancel_form.cancel_reservation()
            success_url = reverse('view_cancel_calendar_message_success'\
                            , kwargs={  'id_hash' : id_hash\
                                    , 'selected_date':  selected_date.strftime('%Y-%m-%d') }\
                            )
            return HttpResponseRedirect(success_url) # Redirect after POST
        else:
            pass
    else:
        cancel_form = CalendarEventCancellationForm()    
        cancel_form.init(id_hash)
    
    lu.update({'cancel_form' :cancel_form })
    return render_to_response('admin_cancel/cancel_signup.html', lu, context_instance=RequestContext(request))
        
        

        
        
        
        
        
        
        
        
        
