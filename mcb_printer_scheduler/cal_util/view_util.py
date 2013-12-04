from calendar_user.models import CalendarUser
from django.conf import settings


def get_common_lookup(request, **kwargs):
    try:
        HU_PIN_LOGIN_APP_NAME = settings.HU_PIN_LOGIN_APP_NAME
    except:
        HU_PIN_LOGIN_APP_NAME = 'no-pin-app-name-in-settings'  
    
    
    if request is None or not request.user.is_authenticated():
        return { 'calendar_user' : None\
                , 'HU_PIN_LOGIN_APP_NAME' : HU_PIN_LOGIN_APP_NAME\
                , 'mcbgraphics_email' : settings.MCB_GRAPHICS_EMAIL }   # just to be sure

    try:
        calendar_user = CalendarUser.objects.get(user=request.user)
    except CalendarUser.DoesNotExist:
        calendar_user = None
        
        
    lu = { 'calendar_user' : calendar_user\
        ,  'mcbgraphics_email' : settings.MCB_GRAPHICS_EMAIL\
        , 'HU_PIN_LOGIN_APP_NAME' : HU_PIN_LOGIN_APP_NAME\
        }
    return lu
    
