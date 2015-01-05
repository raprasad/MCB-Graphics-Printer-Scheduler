import re

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

@login_required
def view_reservation_history(request, id_hash):
    if id_hash is None:
        raise Http404('History not found.')

    if not request.user.is_authenticated():
        lu.update({ 'ERR_found' : True, 'ERR_not_authenticated' : True })
        return render_to_response('reservation_history/view_user_history.html', 
                                  lu, context_instance=RequestContext(request))

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
        return render_to_response('reservation_history/view_user_history.html', 
                                  lu, context_instance=RequestContext(request))

    reservations = Reservation.objects.select_related(\
                                'user', 'print_media'\
                            ).filter(user=cal_user_to_check\
                                   # , is_cancelled=False\
                                    )
    
    cancellations = Reservation.objects.select_related(\
                                'user', 'print_media'\
                            ).filter(user=cal_user_to_check\
                                    , is_cancelled=True\
                                    )

    stati = Status.objects.all().order_by('sort_order')
    
    lu.update({ 'reservations' : reservations, 
                'cancellations_count' :cancellations.count(), 
                'cal_user_to_check' : cal_user_to_check,
                'stati': stati })

    return render_to_response('reservation_history/view_user_history.html', 
                              lu, context_instance=RequestContext(request))

@login_required
def view_create_invoice(request, res_id):
    if res_id is None:
        raise Http404('Reservation not found.')

    if not request.user.is_authenticated():
        lu.update({ 'ERR_found' : True, 'ERR_not_authenticated' : True })
        return render_to_response('reservation_history/view_user_history.html', 
                                  lu, context_instance=RequestContext(request))

    lu = get_common_lookup(request)
    cal_user = lu.get('calendar_user', None)

    if cal_user.is_calendar_admin:
        pass
    else:
        lu.update({ 'ERR_found' : True, 'ERR_no_permission_to_view_history' : True })
        return render_to_response('reservation_history/view_user_history.html', 
                                  lu, context_instance=RequestContext(request))

    try:
        reservation = Reservation.objects.get(pk=res_id)
    except Reservation.DoesNotExist:
        raise Http404('Reservation not found.')

    bill_date = date.today().strftime("%B %d, %Y")
    m = hashlib.md5()
    m.update(datetime.now().__str__())
    invoice_no = m.hexdigest()[0:10]
    invoice_datestring = reservation.start_datetime.strftime("%Y%m%d_%H%M")
    invoice_code = "%s_%s" % (invoice_datestring, reservation.user.get_user_initials())

    print_media = PrintMediaType.objects.all()

    poster_tube_details = reservation.poster_tube_details
    poster_tube_types = PosterTubeType.objects.all().order_by('name')
    selected_poster_tube_id = None
    selected_poster_tube = None
    for ptype in poster_tube_types:
        if ptype.name in poster_tube_details:
            selected_poster_tube = ptype
            selected_poster_tube_id = ptype.id

    lu.update({'reservation': reservation\
                   , 'bill_date': bill_date\
                   , 'invoice_no': invoice_no\
                   , 'invoice_code': invoice_code\
                   , 'cal_user': cal_user\
                   , 'user_fullname': reservation.user.get_fullname()
                   , 'print_media': print_media
                   , 'poster_tube_id': selected_poster_tube_id
                   , 'poster_tube': selected_poster_tube
                   , 'print_proofing_cost': Decimal(PRINT_PROOFING_COST)
                   , 'tax_rate': Decimal(TAX_RATE)
                   , 'mcb_graphics_email': MCB_GRAPHICS_EMAIL
               })

    if request.method == 'POST':
        frm = CreateInvoiceForm(request.POST)
        lu.update({'form': frm })
        if frm.is_valid():
            frm_data = frm.cleaned_data
            frm_data['note'] = mark_safe(frm_data['note'].replace('\n', '<br />\n'))
            frm_data['note'] = mark_safe("%s<br />\n" % frm_data['note'])
            frm_data['extra'] = mark_safe(frm_data['extra'].replace('\n', '<br />\n'))
            prod_cost = frm_data['print_media'].name
            billing_code = frm_data['billing_code']
            try:
                poster_tube = PosterTubeType.objects.get(pk=frm_data['poster_tube'])
            except:
                try:
                    poster_tube = PosterTubeType.objects.get(name='No Tube')
                except:
                    raise
            cc = frm_data['cc']
            if frm_data['payment_method'] == 'cash':
                billing_code = 'paid with cash'
            lu.update({'fd': frm_data,
                       'cc': cc,
                       'billing_code': billing_code,
                       'prod_cost': prod_cost,
                       'poster_tube': poster_tube })
            if frm_data['download_pdf'] == "True":
                return view_save_invoice(request, lu)
            return view_preview_invoice(request, lu)
        return render_to_response('reservation_history/view_form_create_invoice.html',
                                  lu, context_instance=RequestContext(request))
    else:
        note_array = [reservation.note]
        note_array = filter(None, note_array)
        note_string = '\n'.join(note_array)
        initial_form_data = {'note': note_string,
                             'billing_date': datetime.now(),
                             'completed_date': reservation.last_update,
                             'print_proofing_cost': PRINT_PROOFING_COST,
                             'sq_feet': 0.0}
        if reservation.print_media != None:
            initial_form_data.update({'print_media': reservation.print_media})

        if reservation.poster_tube_details != None:
            initial_form_data.update({'poster_tube': selected_poster_tube_id})

        if reservation.billing_code != None:
            initial_form_data.update({'billing_code': reservation.billing_code})
            
        frm = CreateInvoiceForm(instance=reservation,
                                initial=initial_form_data)
    lu.update({ 'form': frm })
    return render_to_response('reservation_history/view_form_create_invoice.html',
                                      lu, context_instance=RequestContext(request))

@login_required
def view_preview_invoice(request, lu):
    return render_to_response('reservation_history/view_preview_invoice.html',
                              lu, context_instance=RequestContext(request))

@login_required
def view_save_invoice(request, lu):
    reservation = lu['reservation']
    invoice_no = lu['invoice_no']
    datestring = reservation.start_datetime.strftime("%Y%m%d_%H%M")
    filename = "%s_%s.pdf" % (datestring, reservation.user.get_user_initials())
    html = render_to_string('reservation_history/view_download_pdf.html',
                            lu, context_instance=RequestContext(request))
    invoice = Invoice(reservation=reservation,
                      invoice_no=invoice_no,
                      filename=filename,
                      html=html)
    invoice.save()
    
    return download_invoice(request, filename, lu)

def view_display_invoice(request, invoice_no):
    invoice = get_object_or_404(Invoice, invoice_no=invoice_no)
    lu = {'invoice': invoice}
    return render_to_response('reservation_history/view_display_invoice.html',
                              lu, context_instance=RequestContext(request))

def download_invoice(request, filename, lu):

    #lu = get_common_lookup(request)
    cal_user = lu.get('calendar_user', None)

    if cal_user.is_calendar_admin:
        pass
    else:
        lu.update({ 'ERR_found' : True, 'ERR_no_permission_to_view_history' : True })
        return render_to_response('reservation_history/view_user_history.html', 
                                  lu, context_instance=RequestContext(request))

    invoice = get_object_or_404(Invoice, invoice_no=lu['invoice_no'])

    #first delete previous invoices
    cmd = 'rm -f /tmp/*.pdf'
    p = Popen(cmd, stdout=PIPE, shell=True)
    output = p.communicate()

    url = 'http://mcbweb.unix.fas.harvard.edu/poster-printer/history/display-invoice/%s/' % (lu['invoice_no'])
    filepath = '/tmp/%s' % filename
    cmd  = '/usr/local/bin/wkhtmltopdf.sh %s %s' % (url, filepath)
    p = Popen(cmd, stdout=PIPE, shell=True)
    output = p.communicate()

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
    from_email = MCB_GRAPHICS_EMAIL
    to = [cal_user.get_email()]
    email_separator = re.compile(r'[,;]+')
    cc_list = email_separator.split(lu['cc'])
    for email in cc_list:
        to.append(email)

    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.attach_file(filepath)
    msg.send()

    #filename = "/vagrant/MCB-Graphics-Printer-Scheduler/email_log/email%s.txt" % datetime.now().strftime("%y%m%d_%H%M%S")
    #email_filename = "/vagrant/MCB-Graphics-Printer-Scheduler/email_log/download_invoice_%s.html" % datetime.now().strftime("%y%m%d_%H%M%S")
    #with open(email_filename, "w") as f:
    #    f.write(html_content)


    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename

    return response

@login_required
def view_mark_status(request, res_id, status):
    if res_id is None:
        raise Http404('Reservation not found.')

    if not request.user.is_authenticated():
        lu.update({ 'ERR_found' : True, 'ERR_not_authenticated' : True })
        return render_to_response('reservation_history/view_user_history.html', 
                                  lu, context_instance=RequestContext(request))

    lu = get_common_lookup(request)
    cal_user = lu.get('calendar_user', None)

    if cal_user.is_calendar_admin:
        pass
    else:
        lu.update({ 'ERR_found' : True, 'ERR_no_permission_to_view_history' : True })
        return render_to_response('reservation_history/view_user_history.html', 
                                  lu, context_instance=RequestContext(request))

    try:
        reservation = Reservation.objects.get(pk=res_id)
    except Reservation.DoesNotExist:
        raise Http404('Reservation not found.')

    try:
        reservation.status = Status.objects.get(name=status)
        reservation.save()
    except:
        raise Http404('Problem setting reservation status')

    cal_admin = cal_user
    cal_user = reservation.user
    lu.update({'cal_event': reservation.calendarevent_ptr, 'cal_user': cal_user, 'cal_admin': cal_admin, 'hostname': request.get_host(), 'static_url': STATIC_URL})
    plaintext = get_template('email/%s.txt' % status)
    htmly     = get_template('email/%s.html' % status)
    d = Context(lu)
    if status == 'received':
        subject = 'Your image file has been received.'
    if status == 'finished':
        subject = 'Your Poster has been printed'
    from_email, to = MCB_GRAPHICS_EMAIL, cal_user.get_email()
    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    #filename = "/vagrant/MCB-Graphics-Printer-Scheduler/email_log/email%s.txt" % datetime.now().strftime("%y%m%d_%H%M%S")
    #filename = "/vagrant/MCB-Graphics-Printer-Scheduler/email_log/email%s.html" % datetime.now().strftime("%y%m%d_%H%M%S")
    #with open(filename, "w") as f:
    #    f.write(html_content)

    return redirect(reverse('view_reservation_history', kwargs={'id_hash': reservation.user.id_hash}))

@login_required
def view_mark_timeslot_free(request, res_id, status):
    if res_id is None:
        raise Http404('Reservation not found.')

    if not request.user.is_authenticated():
        lu.update({ 'ERR_found' : True, 'ERR_not_authenticated' : True })
        return render_to_response('reservation_history/view_user_history.html', 
                                  lu, context_instance=RequestContext(request))

    lu = get_common_lookup(request)
    cal_user = lu.get('calendar_user', None)

    if cal_user.is_calendar_admin:
        pass
    else:
        lu.update({ 'ERR_found' : True, 'ERR_no_permission_to_view_history' : True })
        return render_to_response('reservation_history/view_user_history.html', 
                                  lu, context_instance=RequestContext(request))

    try:
        cal_event = CalendarEvent.objects.get(pk=res_id)
    except CalendarEvent.DoesNotExist:
        raise Http404('Cal Event not found.')

    #only make boolean true if the string "True" is passed
    if status == 'True':
        status = True
    else:
        status = False

    try:
        cal_event.is_timeslot_free = status
        cal_event.save()
    except:
        raise Http404('Problem setting calendar event')

    return redirect(reverse('view_reservation_history', kwargs={'id_hash': cal_event.reservation.user.id_hash}))
