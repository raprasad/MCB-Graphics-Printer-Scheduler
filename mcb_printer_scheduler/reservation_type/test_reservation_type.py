import sys
from datetime import datetime, time, timedelta
import unittest
from django.test import TestCase
from calendar_event.models import CalendarEvent
from reservation_type.models import ReservationType
import python_version
#python manage.py dumpdata reservation_type calendar_event --indent=4 > reservation_type/fixtures/test_reservation_type_fixture_01.json

def msg(m): print m
def dashes(): msg('-' * 40)
def msgt(m): dashes(); msg(m); dashes()
def msgx(m): msgt(m); print 'exiting...'; sys.exit(0)

class ReservationTypeTest(TestCase):
    fixtures = ['test_reservation_type_fixture_01.json']
  
    def setUp(self):
        pass
        
    def runTest(self):
        #--------------------------------------------
        time_now = datetime.now()
        
        #--------------------------------------------
        evt = CalendarEvent.objects.get(pk=1)
        msgt('Should be 20 minute calendar event, actual count: [%s]' % (evt.get_event_length_in_minutes()))
        self.assertEqual(evt.get_event_length_in_minutes(), 20)

        msgt('ISO day of week should be 4 for Thursday. [%s]' % (evt.start_time.isoweekday()))
        self.assertEqual(evt.start_time.isoweekday(), 4)
        
        #--------------------------------------------
        rt = ReservationType.objects.get(pk=1)
        msgt('ReservationType time_block should be 20 minutes, actual: [%s]' % (rt.time_block))
        self.assertEqual(rt.time_block, 20)

        #--------------------------------------------

        #rt.set_day_iso_numbers()
        print 'day_iso_numbers', rt.day_iso_numbers
        rt.save()
        msgt('Calendar event should be valid for reservation type  Actual: %s' % (rt.is_calendar_event_valid(evt)))
        self.assertEqual(rt.is_calendar_event_valid(evt), True)

        #--------------------------------------------
        rt.time_block = 30
        msgt('Change time block to 30 minuts.  Calendar event should be --invalid-- for reservation type.  Actual: %s' % (rt.is_calendar_event_valid(evt)))
        self.assertEqual(rt.is_calendar_event_valid(evt), False)
