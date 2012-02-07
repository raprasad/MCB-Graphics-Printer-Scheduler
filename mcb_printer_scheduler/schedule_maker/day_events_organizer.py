import datetime

class DayEvents:
    def __init__(self, date, events=None, current_date=None):
        self.date = date    # date object
        self.events = events

        # date flags
        self.is_day_future = False
        self.is_day_today = False
        self.is_day_past = False
        self.is_date_other_month = False

        self.set_date_flags(current_date)
        
    def set_date_flags(self, current_date):
        if current_date is None:
            return
            
        if self.date < current_date:
            self.is_day_past = True
        elif self.date > current_date:
            self.is_day_future = True
        else:   # date is current date
            self.is_day_today= True
    
        if current_date.year == self.date.year and current_date.month == self.date.month:
            pass
        else:
            self.is_date_other_month = True
        
    def has_events(self):
        if self.get_event_count() > 0:
            return True
        return False
        
    def get_event_count(self):
        if self.events is None:
            return 0
        return len(self.events)
    
    def add_event(self, event):
        if self.events is None:
            self.events = []
        self.events.append(event)
        

class DayEventsOrganizer:
    def __init__(self, cal_weeks, events, current_date=None):
        """Given events and a list of weeks (Date objects).  Replace each Date object with a DayEvents object containing date appropriate events"""
        self.today = datetime.date.today()

        self.current_date = current_date
        if self.current_date is None:
            self.currrent_date = self.today
            
        self.events = events
        self.cal_weeks = cal_weeks

        self.event_lookup = {}
        
        self.organize_event_lookup()
        self.add_events_to_calendar_weeks()
        
    def organize_event_lookup(self):
        if self.events is None or self.event_lookup is None:
            return
            
        for evt in self.events:
            evt_date = evt.start_datetime.date()

            # get DayEvents object exist for this date?
            day_events_obj = self.event_lookup.get(evt_date, DayEvents(evt_date, current_date=self.today))
            # add the event
            day_events_obj.add_event(evt)
            #if day_events_obj.get_event_count() == 1:
            # update the lookup
            self.event_lookup.update( { evt_date:day_events_obj})
            print day_events_obj.date, day_events_obj.events
            
    def add_events_to_calendar_weeks(self):
        fmt_weeks = []
        for week in self.cal_weeks:            
            fmt_week = []
            for day in week:
                day_event_obj = self.event_lookup.get(day, DayEvents(day, current_date=self.today))
                fmt_week.append(day_event_obj)
            fmt_weeks.append(fmt_week)
        self.cal_weeks = fmt_weeks

