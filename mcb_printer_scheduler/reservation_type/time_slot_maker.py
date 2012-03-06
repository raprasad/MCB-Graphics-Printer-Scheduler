from datetime import date, datetime, time, timedelta
from calendar_event.models import CalendarEvent
from calendar_event.calendar_event_helper import CalendarEventOrganizer

from reservation_type.models import ReservationType
from reservation_type.conflict_checker import ConflictChecker
"""
Given a particular day, choose the ReservationType that applies
"""

class OptLabelVal:
    def __init__(self, label, val):
        self.label = label
        self.val = val

class TimeSlot:
    def __init__(self, start_datetime, end_datetime):
        self.check_selected_date_times(start_datetime, end_datetime)
        
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
    
    def get_timeslot_label_for_form(self):
        return '%s' % (self.start_datetime.strftime('%I:%M %p'))

        #return '%s - %s' % (self.start_datetime.strftime('%I:%M %p')\
        #                     ,  self.end_datetime.strftime('%I:%M %p'))

    def get_start_time_for_form(self):
        label = '%s' % (self.start_datetime.strftime('%I:%M %p'))
        val = self.start_datetime   #strftime('%Y-%m-%d %H:%M')
        return (val, label)

    def get_end_time_for_ajax_call(self):
         label = '%s' % (self.end_datetime.strftime('%I:%M %p'))
         val = self.end_datetime.strftime('%Y-%m-%d %H:%M')
         return OptLabelVal(label, val)

    def get_end_time_for_form(self):
        label = '%s' % (self.end_datetime.strftime('%I:%M %p'))
        val = self.end_datetime   #strftime('%Y-%m-%d %H:%M')
        return (val, label)
        

    def get_timeslot_entry_for_form(self):
        label = self.get_timeslot_label_for_form()
        val = self.start_datetime   #strftime('%Y-%m-%d %H:%M')
        return (val, label)

    def check_selected_date_times(self, start_datetime, end_datetime):
        """Check that datetime objects are valid and start time isn't after end time"""
        
        if start_datetime is None or not start_datetime.__class__.__name__ == 'datetime':
            raise ValueError('start_datetime is not a datetime.time object!')

        if end_datetime is None or not end_datetime.__class__.__name__ == 'datetime':
            raise ValueError('end_datetime is not a datetime.time object!')

        if start_datetime > end_datetime :
            raise ValueError('start_datetime is greater than the end_datetime')
            
            

class TimeSlotChecker:
    """
    Given a date and the current date:
    - Find the appropriate ReservationType
    - Find the current reservations
    - Return a list of open time slots

    Errors for template use:
    """
    ERR_reservation_type_not_found = False
    ERR_signup_day_has_passed = False
    ERR_selected_date_not_valid_for_reservation_type = False
    ERR_no_reservation_times_left_today = False
    
    def __init__(self, selected_date, calendar_user=None):

        self.selected_date = self.check_selected_date(selected_date)

        self.current_datetime = datetime.now()
        self.current_date  = self.current_datetime.date()
        
        # to hold events for the selected day
        self.calendar_events = None
        
        self.reservation_type = None
        
        self.open_timeslots = []
        self.num_timeslots = 0
        self.err_flags = []
        
        self.init_err_flag_attrs()
        self.gather_calendar_events()   # get events for the selected_date
        self.calculate_time_slots()     # choose reservation type and calculate time slots


    def get_start_time_choices_for_form(self):
        if self.open_timeslots is None or len(self.open_timeslots) == 0:
            return None
        return [('', '------')] + map(lambda x: x.get_start_time_for_form()\
                                , self.open_timeslots)
    
    def get_end_time_choices_for_form(self):
        if self.open_timeslots is None or len(self.open_timeslots) == 0:
            return None
        return [('', '------')] + map(lambda x: x.get_end_time_for_form()\
                                                            , self.open_timeslots)
    
    
    def get_end_times_for_ajax_call(self, start_datetime):
        if start_datetime is None:
            return None
            
        if self.open_timeslots is None or len(self.open_timeslots) == 0:
            return None
        
        # filter out times before the start_datetime
        avail_slots = filter(lambda x: x.end_datetime > start_datetime, self.open_timeslots)
        if len(avail_slots) == 0:
            return None
        
        # remove non-contiguous times
        last_end = None
        contiguous_times = []
        for idx, ts in enumerate(avail_slots):
            if idx > 0 and not ts.start_datetime == last_end:
                break
            contiguous_times.append(ts)
            last_end = ts.end_datetime

        
        return map(lambda x: x.get_end_time_for_ajax_call(), contiguous_times)
    
    def get_timeslot_choices_for_form(self):
        if self.open_timeslots is None or len(self.open_timeslots) == 0:
            return None
        return [('', '------')] + map(lambda x: x.get_timeslot_entry_for_form()\
                            , self.open_timeslots)
                            

    def get_reservation_time_block(self):
        if self.reservation_type is None:
            return None
        return self.reservation_type.time_block

    def get_lookup_for_template(self):

        lu = { 'selected_date' : self.selected_date\
                , 'calendar_events' : self.calendar_events\
                , 'current_datetime' : self.current_datetime\
                , 'current_date' : self.current_date\
                , 'reservation_type' : self.reservation_type\
                , 'selected_date' : self.selected_date\
                , 'open_timeslots' : self.open_timeslots\
                , 'num_timeslots' : self.num_timeslots\
                }
                
        lu.update(self.get_err_flag_lookup())
        return lu
        
    def err_found(self):
        for attr in self.__dict__.keys():
            if attr.startswith('ERR_'):
                if self.__dict__.get(attr, False) is True:
                    return True
        return False
                
    def init_err_flag_attrs(self):
        for attr in self.__dict__.keys():
            if attr.startswith('ERR_'):
                self.__dict__.update({ attr : False })


    def get_err_flag_lookup(self):
        lu = {}
        for attr in self.__dict__.keys():
            if attr.startswith('ERR_'):
               lu.update({ attr : self.__dict__.get(attr, False) })
        return lu

    def check_selected_date(self, selected_date):
        if selected_date is None or not selected_date.__class__.__name__ == 'date':
            raise ValueError('selected_date is not a datetime.date object!')
        return selected_date
        

    def add_err_flag(self, m):
        if m is None:
            return
        self.err_found = True
        self.err_flags.append(m)
    
    def gather_calendar_events(self):
        cal_events = CalendarEvent.objects.filter(is_visible=True\
                             , start_datetime__gte=datetime.combine(self.selected_date, time.min)
                             , start_datetime__lte=datetime.combine(self.selected_date, time.max)).order_by('start_datetime')
        
        self.calendar_events = CalendarEventOrganizer.substitute_cal_event_subclasses(cal_events)
        
    def check_for_conflict(self, timeslot):
        if timeslot is None:
            raise ValueError('None timeslot object sent.')
            
        if self.calendar_events is None:        # Nothing to conflict with?
            return False
        
        """Check for conflicts"""
        #for cal_event in self.calendar_event:
        #    if 

    def calculate_time_slots(self):
        
        if self.selected_date < self.current_date:        
             self.ERR_signup_day_has_passed = True
             return
        
        self.reservation_type = TimeSlotChecker.choose_reservation_type_by_date(self.selected_date, self.current_date)
        if self.reservation_type is None:
            self.ERR_reservation_type_not_found = True
            return
            
        if self.current_datetime >= datetime.combine(self.selected_date, self.reservation_type.closing_time):
            self.ERR_facility_closed = True
            return
                
        # set initial time slot
        start_datetime = datetime.combine(self.selected_date, self.reservation_type.opening_time)
        end_datetime = start_datetime + timedelta(minutes=self.reservation_type.time_block)
        
        conflict_checker = ConflictChecker()    # helps check against all existing CalendarEvents
        while end_datetime.time() <= self.reservation_type.closing_time:
            timeslot = TimeSlot(start_datetime, end_datetime)
            
            if not conflict_checker.does_timeslot_conflict(timeslot):
                # make sure the time slot hasn't passed--if it's the current day
                if start_datetime >= self.current_datetime:
                    self.open_timeslots.append(timeslot)
            # set next timeslot
            start_datetime = end_datetime
            end_datetime = start_datetime + timedelta(minutes=self.reservation_type.time_block)
        
        self.num_timeslots = len(self.open_timeslots)

        if self.num_timeslots == 0:
            self.ERR_no_reservation_times_left_today = True
            
    

    @staticmethod
    def choose_reservation_type(date_str):
        """Choose reservation type by date string in formats
            YYYY-mm-dd
            YYYY/mm/dd
        """
        if date_str is None:
            return None

        try:
            date_str = date_str.replace('/', '-')
            selected_date = date.strptime(date_str, '%Y-%m-%d')
            return choose_reservation_type_by_date(selected_date)
        except:
            return None

    @staticmethod
    def choose_reservation_type_by_date(selected_date, current_date):
        """
        Given a date, choose the corresponding ReservationType object, assuming there is one
        """
        if selected_date is None:
            return None

        qset = ReservationType.objects.filter(is_active=True) 

        l = filter(lambda x: x.is_potential_reservation_date_valid(selected_date, current_date), qset)
        if len(l) > 0:
            return l[0]

        return None







