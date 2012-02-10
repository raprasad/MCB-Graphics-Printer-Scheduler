from calendar_event.models import *

class CalendarEventOrganizer:
    """if it exists, replace a CalendarEvent with it's subclass"""
    
    @staticmethod
    def substitute_cal_event_subclasses(cal_events):
        if cal_events is None:
            return None

        # retrieve node subclass names.  e.g.: "CalendarEvent", "Reservation", etc
        subclass_dict = {}  # { subclass name : 1 }
        map(lambda x: subclass_dict.update({x.subclass_name:1}), cal_events)

        # retrieve CalendarEvent ids
        cal_event_ids = map(lambda x: x.id, cal_events)

        # build a lookup of CalendarEvent subclass instances { cal_id : instance of subclass }; 
        #
        cal_event_subclass_objects = {}  
        for subclass_name in subclass_dict.keys():  # iterate through node subclass names

            if (not subclass_name) or subclass_name == '':
                continue    # go to the next subclass name
            cal_evt_obj_type = eval(subclass_name)     # e.g. eval('Page')
            # retrieve subclass instances
            subclass_object_qs = cal_evt_obj_type.objects.select_related().filter(id__in=cal_event_ids, is_visible=True) 
            # put subclass instances into lookup
            for subclass_obj in subclass_object_qs:  
                cal_event_subclass_objects.update({ subclass_obj.id: subclass_obj })

        # Iterate through the nodes and, if subclass available, REPLACE with the appropriate 'subclass'
        #
        formatted_cal_evts = []
        for nd in cal_events:
            # if subclass is available, replace the node with its subclass
            #formatted_cal_evts.append(cal_event_subclass_objects.get(nd.id, nd))
            subclass_obj = cal_event_subclass_objects.get(nd.id, None)
            if subclass_obj:
                formatted_cal_evt = subclass_obj
            else:   # subclass not found, use the CalendarEvent
                formatted_cal_evt = nd

            formatted_cal_evts.append(formatted_cal_evt)      
        return formatted_cal_evts
