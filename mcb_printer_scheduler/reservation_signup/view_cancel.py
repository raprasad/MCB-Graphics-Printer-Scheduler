from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from calendar_event.models import CalendarEvent, Reservation
from reservation_type.time_slot_maker import TimeSlotChecker
from reservation_signup.forms_cancel import ReservationCancellationForm
from reservation_signup.email_notification import  mail_billing_code_reminder

from cal_util.view_util import get_common_lookup
from cal_util.msg_util import *

from django.core.urlresolvers import reverse

@login_required
def view_cancel_success(request, id_hash):
    if id_hash is None:
        raise Http404('Reservation not found.')


    if not request.user.is_authenticated():
        lu.update({ 'ERR_found' : True, 'ERR_not_authenticated' : True })
        return render_to_response('reservation_signup/cancel_signup_success.html', lu, context_instance=RequestContext(request))

    try:
        reservation = Reservation.objects.get(id_hash=id_hash)
    except Reservation.DoesNotExist:
        raise Http404('Reservation not found.')


    lu = get_common_lookup(request)
    cal_user = lu.get('calendar_user', None)

    if cal_user.is_calendar_admin or (cal_user == reservation.user):
        pass
    else:
        lu.update({ 'ERR_found' : True, 'ERR_no_permission_to_cancel' : True })
        return render_to_response('reservation_signup/cancel_signup_success.html', lu, context_instance=RequestContext(request))
        

    lu.update({'reservation' : reservation
            , 'selected_date' : reservation.start_datetime.date() })

    timeslot_checker = TimeSlotChecker(selected_date=reservation.start_datetime.date())
    lu.update({ 'calendar_events' : timeslot_checker.calendar_events })

    if not reservation.is_cancelled:
        lu.update({ 'ERR_found' : True, 'ERR_reservation_not_cancelled' : True })
        return render_to_response('reservation_signup/cancel_signup_success.html', lu, context_instance=RequestContext(request))

    lu.update({ 'cancel_success' : True })
    return render_to_response('reservation_signup/cancel_signup_success.html', lu, context_instance=RequestContext(request))
    
    
@login_required    
def view_code_reminder(request, id_hash):
    import logging
    log = logging.getLogger(__name__)

    if id_hash is None:
        raise Http404('Reservation not found.')
    
    if not request.user.is_authenticated():
        lu.update({ 'ERR_found' : True, 'ERR_not_authenticated' : True })
        return render_to_response('reservation_signup/cancel_signup.html', lu, context_instance=RequestContext(request))
    
    try:
        reservation = Reservation.objects.get(id_hash=id_hash, is_visible=True)
    except Reservation.DoesNotExist:
        raise Http404('Reservation not found.')
    
    lu = get_common_lookup(request)
    cal_user = lu.get('calendar_user', None)

    log.info("USER %s"%cal_user)
    log.info("USER %s"%cal_user.contact_email)

    lu.update({'reservation' : reservation
            , 'email' : cal_user.contact_email
            , 'selected_date' : reservation.start_datetime.date() })
    
    cal_user = lu.get('calendar_user')

    mail_billing_code_reminder(reservation,cal_user.contact_email)
  
    return render_to_response('reservation_signup/code_reminder.html', lu, context_instance=RequestContext(request))

@login_required    
def view_cancel_signup(request, id_hash):
    import logging
    log = logging.getLogger(__name__)
    log.info("HERE")
    if id_hash is None:
        raise Http404('Reservation not found.')
    
    if not request.user.is_authenticated():
        lu.update({ 'ERR_found' : True, 'ERR_not_authenticated' : True })
        return render_to_response('reservation_signup/cancel_signup.html', lu, context_instance=RequestContext(request))
    
    try:
        reservation = Reservation.objects.get(id_hash=id_hash, is_visible=True)
    except Reservation.DoesNotExist:
        raise Http404('Reservation not found.')
    
    lu = get_common_lookup(request)
    cal_user = lu.get('calendar_user', None)

    if cal_user.is_calendar_admin or (cal_user == reservation.user):
        pass
    else:
        lu.update({ 'ERR_found' : True, 'ERR_no_permission_to_cancel' : True })
        return render_to_response('reservation_signup/cancel_signup.html', lu, context_instance=RequestContext(request))

    if reservation.is_cancelled:    # should never happen b/c shouldn't be visible
        lu.update({ 'ERR_found' : True, 'ERR_reservation_already_cancelled' : True })
        return render_to_response('reservation_signup/cancel_signup.html', lu, context_instance=RequestContext(request))



    lu.update({'reservation' : reservation
            , 'selected_date' : reservation.start_datetime.date() })
    
    timeslot_checker = TimeSlotChecker(selected_date=reservation.start_datetime.date())
    lu.update({ 'calendar_events' : timeslot_checker.calendar_events })

    cal_user = lu.get('calendar_user')
        
    
    if request.method == 'POST': # If the form has been submitted...
        cancel_form = ReservationCancellationForm(request.POST) # A form bound to the POST data
        if cancel_form.is_valid(): # All validation rules pass
            
            res = cancel_form.cancel_reservation()
            
            success_url = reverse('view_cancel_success'\
                            , kwargs={  'id_hash' : res.id_hash }\
                            )
            return HttpResponseRedirect(success_url) # Redirect after POST
        else:
            pass
    else:
        cancel_form = ReservationCancellationForm()    
        cancel_form.init(id_hash)

    lu.update({'cancel_form' :cancel_form })
    return render_to_response('reservation_signup/cancel_signup.html', lu, context_instance=RequestContext(request))
        
        

        
        
        
        
        
        
