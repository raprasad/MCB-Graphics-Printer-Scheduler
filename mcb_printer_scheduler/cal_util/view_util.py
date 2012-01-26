from calendar_user.models import CalendarUser



def get_common_lookup(request, **kwargs):
    if request is None:
        return {}

    user = request.user
    try:
        calendar_user = CalendarUser.objects.get(user=user)
    except CalendarUser.DoesNotExist:
        user = None
        
    lu = { 'cal_user' : cal_user }
    return lu
    
