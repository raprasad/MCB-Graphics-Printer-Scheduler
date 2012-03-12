import os
import sys

sys.stdout = sys.stderr     # send print statements to the apache logs

prod_paths = ['/home/p/r/prasad/webapps/django/MCB-Graphics-Printer-Scheduler'\
    , '/home/p/r/prasad/webapps/django/MCB-Graphics-Printer-Scheduler/mcb_printer_scheduler']

for p in prod_paths:
    if os.path.isdir(p): sys.path.append(p)

os.environ['DJANGO_SETTINGS_MODULE'] = 'mcb_printer_scheduler.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

