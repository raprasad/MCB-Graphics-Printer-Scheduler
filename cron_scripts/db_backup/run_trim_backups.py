import os, sys

sys.path.append('/home/p/r/prasad/webapps/django/MCB-Graphics-Printer-Scheduler/mcb_printer_scheduler')
sys.path.append('/home/p/r/prasad/webapps/django/MCB-Graphics-Printer-Scheduler')

from mcb_printer_scheduler import settings
from django.core.management import setup_environ
setup_environ(settings)

# pull in "BackupMaker"
sys.path.append('/home/p/r/prasad/webapps/django/mcb_lib/poor-mans-db-backup')
from backupdb.trim_backups import BackupTrimmer


if __name__=='__main__':
   bt = BackupTrimmer(backup_name='Poster Printer')
   #bt.make_test_directories(num_dirs=20)
   bt.run_trimmer()
