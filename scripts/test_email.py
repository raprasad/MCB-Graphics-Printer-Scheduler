import os
import sys

PROJECT_DIR = os.path.join(os.path.dirname(__file__), '../')
sys.path.append(PROJECT_DIR)
sys.path.append(os.path.join(PROJECT_DIR, 'mcb_printer_scheduler'))

import settings
from django.core.management import setup_environ
setup_environ(settings)

from django.template import Context
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

from settings import STATIC_URL, MCB_GRAPHICS_EMAIL
from calendar_event.models import Reservation
from calendar_user.models import CalendarUser

def send_email(filename):
    lu = {}
    filedir = "/home/p/r/prasad/webapps/django/MCB-Graphics-Printer-Scheduler/media/"
    filepath = os.path.join(filedir, filename)

    pdf_data = open(filepath, "rb").read()

    cal_admin = CalendarUser.objects.get(pk=1384)
    reservation = Reservation.objects.get(pk=3935)
    cal_user = reservation.user
    lu.update({'cal_event': reservation.calendarevent_ptr,
               'cal_user': cal_user,
               'cal_admin': cal_admin,
               'hostname': 'http://mcbweb.unix.fas.harvard.edu',
               'static_url': STATIC_URL})
    plaintext = get_template('email/download_pdf.txt')
    htmly     = get_template('email/download_pdf.html')
    d = Context(lu)
    subject = 'Invoice copy from MCB Graphics 1'
    from_email, to = MCB_GRAPHICS_EMAIL, 'mattison@g.harvard.edu'
    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.attach_file(filepath)
    msg.send()     

if __name__ == "__main__":
    send_email("20140919_1215_EM.pdf")
