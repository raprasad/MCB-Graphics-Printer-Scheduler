from calendar_user.models import CalendarUser
from django.conf import settings


def get_common_lookup(request, **kwargs):
    if request is None or not request.user.is_authenticated():
        return { 'calendar_user' : None\
                , 'mcbgraphics_email' : settings.MCB_GRAPHICS_EMAIL }   # just to be sure

    try:
        calendar_user = CalendarUser.objects.get(user=request.user)
    except CalendarUser.DoesNotExist:
        calendar_user = None
        
    lu = { 'calendar_user' : calendar_user
        ,  'mcbgraphics_email' : settings.MCB_GRAPHICS_EMAIL}
    return lu
    
