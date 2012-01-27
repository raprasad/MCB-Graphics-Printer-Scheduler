from django.conf import settings 
import sys
def msg(m): 
    if settings.DEBUG: print m
def dashes(): msg('-'*40)
def msgt(m): dashes(); msg(m); dashes()
def msgx(m): dashes(); msg(m); msg('exiting..'); sys.exit(0)