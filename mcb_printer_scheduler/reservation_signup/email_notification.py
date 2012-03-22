from django.conf import settings 
from django.template.loader import render_to_string
from django.core.mail import send_mail

def notify_staff_of_last_minute_reservation(reservation):
    if reservation is None:
        return 
    
    subject = '%s: Last minute reservation' % (reservation.user.get_fullname())

    msg = render_to_string('reservation_signup/email_last_minute_signup.txt', { 'reservation':reservation})

    send_mail(subject, msg, settings.MCB_GRAPHICS_EMAIL\
            , [ settings.MCB_GRAPHICS_EMAIL], fail_silently=False)
