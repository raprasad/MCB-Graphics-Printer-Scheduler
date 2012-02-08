from calendar_event.models import CalendarEvent

class ConflictChecker:
    """
    proposed_timeslot: requires start_datetime and end_datetime objects
    """
    def __init__(self, event_to_edit=None):        

        self.event_to_edit = event_to_edit
        
        if event_to_edit:
            self.base_evts = CalendarEvent.objects.filter(is_visible=True).exclude(id=event_to_edit.id)
        else:
            self.base_evts = CalendarEvent.objects.filter(is_visible=True)
    
    def does_timeslot_conflict(self, proposed_timeslot):

        if proposed_timeslot is None:
            raise ValueError('ConflictChecker - proposed_timeslot is None')
        if proposed_timeslot.__dict__.get('start_datetime', None) is None:
            raise ValueError('ConflictChecker - proposed_timeslot has no start_datetime')
        if proposed_timeslot.__dict__.get('end_datetime', None) is None:
            raise ValueError('ConflictChecker - proposed_timeslot has no end_datetime')
     
        # new_start - proposed start time
        # new_end - proposed end time
        # existing_start - scheduled start time
        # existing_end - scheduled end time
        
        # 1- check if previous session ended during the new session 
        #   (a) new_start  existing_end  new_end
        #   (b) new_start  existing_end|new_end 
        check1_evts = self.base_evts.filter(end_datetime__gt=proposed_timeslot.start_datetime\
                                    , end_datetime__lte=proposed_timeslot.end_datetime\
                                    )
        if check1_evts.count() > 0:
            return True
   
        # 2- check if a previous session started during the new session 
        #   (a)        new_start   existing_start   new_end
        #   (b)        existing_start|new_start    new_end
        check2_evts = self.base_evts.filter(start_datetime__gte=proposed_timeslot.start_datetime\
                                    , start_datetime__lt=proposed_timeslot.end_datetime\
                                    )
        if check2_evts.count() > 0:
            return True

        # 3- check if previous session "encompassed" the new session  
        #   (a) existing_start  new_start   new_end     existing_end
        #   x(b) existing_start|new_start   new_end     existing_end (caught in check #1)
        #   x(c) existing_start  new_start   new_end|existing_end    (caught in check #1)
        #   x(d) existing_start|new_start   new_end|existing_end     (caught in check #2)
        check3_evts = self.base_evts.filter(start_datetime__lte=proposed_timeslot.start_datetime\
                                    , end_datetime__gte=proposed_timeslot.end_datetime\
                                    )
        if check3_evts.count() > 0:
            return True

        return False
        
        #cal_events = filter(lambda x: x.id not in [conflicting_ids], calendar_events)