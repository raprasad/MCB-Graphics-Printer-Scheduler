from calendar_user.models import CalendarUser



def get_common_lookup(request, **kwargs):
    if request is None or not request.user.is_authenticated():
        return { 'calendar_user' : None }   # just to be sure

    try:
        calendar_user = CalendarUser.objects.get(user=request.user)
    except CalendarUser.DoesNotExist:
        calendar_user = None
        
    lu = { 'calendar_user' : calendar_user }
    return lu
    
