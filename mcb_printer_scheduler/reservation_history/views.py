from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from calendar_event.models import CalendarEvent, Reservation
from calendar_user.models import CalendarUser

from cal_util.view_util import get_common_lookup
from cal_util.msg_util import *

from django.core.urlresolvers import reverse

@login_required
def view_reservation_history(request, id_hash):
    if id_hash is None:
        raise Http404('History not found.')


    if not request.user.is_authenticated():
        lu.update({ 'ERR_found' : True, 'ERR_not_authenticated' : True })
        return render_to_response('reservation_history/view_user_history.html', lu, context_instance=RequestContext(request))

    try:
        cal_user_to_check = CalendarUser.objects.get(id_hash=id_hash)
    except CalendarUser.DoesNotExist:
        raise Http404('Reservation history not found for this user.')

    lu = get_common_lookup(request)
    cal_user = lu.get('calendar_user', None)

    if cal_user.is_calendar_admin or cal_user == cal_user_to_check:
        pass
    else:
        lu.update({ 'ERR_found' : True, 'ERR_no_permission_to_view_history' : True })
        return render_to_response('reservation_history/view_user_history.html', lu, context_instance=RequestContext(request))

    
    lu.update({ 'reservations' : Reservation.objects.filter(user=cal_user_to_check)\
            , 'cancellations' : Reservation.objects.filter(user=cal_user_to_check, is_cancelled=True)\
            , 'cal_user_to_check' : cal_user_to_check})

    return render_to_response('reservation_history/view_user_history.html', lu, context_instance=RequestContext(request))


        
