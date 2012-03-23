import datetime

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from calendar_event.models import CalendarEvent, CalendarMessage
from reservation_type.time_slot_maker import TimeSlotChecker
from admin_signup.forms_adjust_time import AvailableHoursForm

from cal_util.view_util import get_common_lookup

from django.core.urlresolvers import reverse

@login_required
def view_adjust_reservation_type_success(request, selected_date):
    return view_adjust_reservation_type(request, selected_date, new_reservation_time_set=True)

@login_required
def view_adjust_reservation_type(request, selected_date, new_reservation_time_set=False):
    if selected_date is None:
        raise Http404('selected_date is None.')

    lu = get_common_lookup(request)
    lu.update({'success_new_reservation_time_set' : new_reservation_time_set})

    try:
        selected_date = datetime.datetime.strptime(selected_date, '%Y-%m-%d').date()
        lu.update({'selected_date' : selected_date })
    except:
        raise Http404('selected_date date not found.')
    
    lu.update({ 'change_hours' : True })

    if not request.user.is_authenticated():
        lu.update({ 'ERR_found' : True, 'ERR_not_authenticated' : True })
        return render_to_response('admin_signup/change_time_page.html', lu, context_instance=RequestContext(request))

    cal_user = lu.get('calendar_user', None)
    if not cal_user.is_calendar_admin:
        lu.update({ 'ERR_found' : True, 'ERR_no_permission_to_change_time' : True })
        return render_to_response('admin_signup/change_time_page.html', lu, context_instance=RequestContext(request))


    timeslot_checker = TimeSlotChecker(selected_date=selected_date)
    lu.update(timeslot_checker.get_lookup_for_template())

    if request.method == 'POST': # If the form has been submitted...
        change_time_form = AvailableHoursForm(request.POST) # A form bound to the POST data
        if change_time_form.is_valid(): # All validation rules pass
            if change_time_form.make_new_reservation_type():
                success_url = reverse('view_adjust_reservation_type_success'\
                                , kwargs={ 'selected_date' : selected_date.strftime('%Y-%m-%d') })
                return HttpResponseRedirect(success_url) # Redirect after POST
            else:
                change_time_form.init(selected_date)
    else:
        change_time_form = AvailableHoursForm()
        change_time_form.init(selected_date)

    lu.update({ 'change_time_form' : change_time_form})
    

    return render_to_response('admin_signup/change_time_page.html', lu, context_instance=RequestContext(request))
    
    
    
    
    
    
    
    
    
    
    