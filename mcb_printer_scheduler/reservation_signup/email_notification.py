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


def mail_billing_code_reminder(reservation,email):

    if reservation is None:
       return

    if email is None:
       return

    subject = '%s: Billing code reminder for poster-printer reservation %s' % ( reservation.user.get_fullname(), reservation)

    msg = render_to_string('reservation_signup/email_billing_code_reminder.txt', {'reservation': reservation, 'fullname':reservation.user.get_fullname(),'email':email})

    import logging;

    log = logging.getLogger(__name__)

    log.info(email)  
    log.info(subject)  
    log.info(msg)  

    send_mail(subject, msg, settings.MCB_GRAPHICS_EMAIL\
            , [ email, 'mclamp@g.harvard.edu'], fail_silently=False)
