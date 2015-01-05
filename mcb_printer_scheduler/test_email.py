import os
import sys

PROJECT_DIR = os.path.join(os.path.dirname(__file__), '../')
sys.path.append(PROJECT_DIR)
sys.path.append(os.path.join(PROJECT_DIR, 'mcb_printer_scheduler'))


import settings
from django.core.management import setup_environ
setup_environ(settings)

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe

from datetime import datetime, date
import hashlib
from subprocess import Popen, PIPE
from calendar_event.models import CalendarEvent, Status, Reservation
from calendar_user.models import CalendarUser
from invoice.models import Invoice
from reservation_history.forms import CreateInvoiceForm
from media_type.models import PrintMediaType
from poster_tube.models import PosterTubeType

from django.views.generic.base import View
from wkhtmltopdf.views import PDFTemplateResponse
from wkhtmltopdf.utils import wkhtmltopdf

from settings import PRINT_PROOFING_COST, TAX_RATE, STATIC_URL, MCB_GRAPHICS_EMAIL
from decimal import Decimal

from cal_util.view_util import get_common_lookup
from cal_util.msg_util import *
from schedule_viewer.views_calendar import view_month_calendar

from django.core.urlresolvers import reverse

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context


def send_email(filename):

    filepath = os.path.join("/home/p/r/prasad/webapps/django/MCB-Graphics-Printer-Scheduler/media", filename)
    print filepath
    sys.exit()

    pdf_data = open(filepath, "rb").read()

    reservation = invoice.reservation
    cal_admin = cal_user
    cal_user = reservation.user
    lu.update({'cal_event': reservation.calendarevent_ptr, 
               'cal_user': cal_user, 
               'cal_admin': cal_admin, 
               'hostname': request.get_host(), 
               'static_url': STATIC_URL})
    plaintext = get_template('email/download_pdf.txt')
    htmly     = get_template('email/download_pdf.html')
    d = Context(lu)
    subject = 'Invoice copy from MCB Graphics'
    from_email, to = MCB_GRAPHICS_EMAIL, cal_user.get_email()
    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.attach_file(filepath)
    #msg.send()

    #filename = "/vagrant/MCB-Graphics-Printer-Scheduler/email_log/email%s.txt" % datetime.now().strftime("%y%m%d_%H%M%S")
    email_filename = "/vagrant/MCB-Graphics-Printer-Scheduler/email_log/download_invoice_%s.html" % datetime.now().strftime("%y%m%d_%H%M%S")
    with open(email_filename, "w") as f:
        f.write(html_content)


    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename

    return response

if __name__ == "__main__":
    send_email()
