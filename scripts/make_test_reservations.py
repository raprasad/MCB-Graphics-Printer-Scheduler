import os
import sys

PROJECT_DIR = os.path.join(os.path.dirname(__file__), '../')
sys.path.append(PROJECT_DIR)
sys.path.append(os.path.join(PROJECT_DIR, 'mcb_printer_scheduler'))

import settings
from django.core.management import setup_environ
setup_environ(settings)

from datetime import datetime
from cal_util.msg_util import *
from calendar_event.models import *
import calendar
import random

from reservation_type.conflict_checker import ConflictChecker
from reservation_type.time_slot_maker import TimeSlot


random_words = '''The fine particulates, caused by dust or emissions from vehicles, coal combustion, factories and construction sites, are among the most hazardous because they easily penetrate lungs and enter the bloodstream. Chronic exposure increases the risk of cardiovascular ailments, respiratory disease and lung cancer. The Chinese government has monitored exposure levels in 20 cities and 14 other sites, reportedly for as long as five years, but has kept the data secret.

It sought 18 months ago to silence the American Embassy in Beijing as well, arguing that American officials had insulted the Chinese government by posting readings from the PM 2.5 monitor atop the embassy on Twitter. A Foreign Ministry official warned that the embassy's data could lead to "social consequences" in China and asked the embassy to restrict access to it. The embassy refused, and Chinese citizens now translate and disseminate the readings widely.

While China has made gains on some other airborne toxins, the PM 2.5 data is far from reassuring in a country that annually has hundreds of thousands of premature deaths related to air pollution. In an unreleased December report relying on government data, the World Bank said average annual PM 2.5 concentrations in northern Chinese cities exceeded American limits by five to six times as much, and two to four times as much in southern Chinese cities.'''.split()

def get_random_initials():
    alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
             
    return '%s%s' % (alpha[random.randint(0,25)], alpha[random.randint(0,25)])
    
def make_reservations(year=2012, month=2, cnt=10):
    global random_words
    iso_day_of_week, num_days_in_month = calendar.monthrange(year, month)
    conflict_checker = ConflictChecker()

    for x in range(1, cnt+1):

        desc_idx_start = random.randint(0, len(random_words)-5)
        rand_desc = ' '.join(random_words[desc_idx_start:desc_idx_start+5])
        
        start_datetime = None
        end_datetime = None
        time_conflicts = True
        while time_conflicts: 
            day_of_week = random.randint(1, num_days_in_month)    
            start_hr = random.randint(0, 23)
            start_min = [0, 20, 40][random.randint(0, 2)]
            start_datetime = datetime(year, month, day_of_week, start_hr, start_min)
            end_datetime = start_datetime + timedelta(minutes=20)
            if not conflict_checker.does_timeslot_conflict(TimeSlot(start_datetime, end_datetime)):
                time_conflicts = False
                
        evt = CalendarEvent(start_datetime=start_datetime\
                    , display_name=get_random_initials()
                    , end_datetime=end_datetime\
                    )
        #            , display_name=rand_desc )
        evt.save()
        print '(%s) evt saved: %s' % (x, evt)

if __name__=='__main__':
    try:
        CalendarEvent.objects.all().delete()
    except:
        for evt in CalendarEvent.objects.all(): evt.delete()
        
    for mth in range(2, 4):
        make_reservations(2012, mth, cnt=55)