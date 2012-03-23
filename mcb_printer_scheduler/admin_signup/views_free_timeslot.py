from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from calendar_event.models import Reservation, CalendarEvent
from cal_util.view_util import get_common_lookup

from django.core.urlresolvers import reverse


@login_required    
def view_free_timeslot(request, id_hash):
    """Mark the CalendarEvent attribute 'is_timeslot_free' as True"""
    # is id_hash specified
    if id_hash is None:
        raise Http404('Reservation not found.')

    lu = get_common_lookup(request)

    # get event
    try:
        cal_event = CalendarEvent.objects.get(id_hash=id_hash, is_visible=True)
        selected_date = cal_event.start_datetime.date()
        lu.update({ 'selected_date' : selected_date})
    except CalendarEvent.DoesNotExist:
        raise Http404('CalendarEvent not found.')
    
    cal_user = lu.get('calendar_user', None)

    # admin check 
    if not cal_user.is_calendar_admin:
        lu.update({ 'ERR_found' : True, 'ERR_no_permission_to_free_timeslot' : True })
        return render_to_response('admin_signup/reservation_signup_page.html', lu, context_instance=RequestContext(request))


    # free timeslot
    cal_event.is_timeslot_free = True
    cal_event.save()
    
    
    
    signup_url = reverse('view_admin_signup_page'\
                    , kwargs={ 'selected_date' : selected_date.strftime('%Y-%m-%d') })

    return HttpResponseRedirect(signup_url) # Redirect after POST
