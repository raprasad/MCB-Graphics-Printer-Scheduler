

class CalendarEventOrganizer:
    """if it exists, replace a CalendarEvent with it's subclass"""
    
    @staticmethod
    def add_calendar_event_subclasses(calendar_events):
        if calendar_events is None:
            return calendar_events

        # retrieve node subclass names.  e.g.: "Page", "PageDirect", "PageCustomView", etc
        subclass_dict = {}  # { subclass name : 1 }
        map(lambda x: subclass_dict.update({x.subclass_name:1}), calendar_events)

        # retrieve node ids
        event_ids = map(lambda x: x.id, calendar_events)

        # build a lookup of Node subclass instances { node_id : instance of subclass }; 
        #   e.g. { 31: <Page: yellow>, 32: <Page: banana>,29: <PageDirect: www.google.com>, 30: <Page: cherry>}
        #
        evt_subclass_objects = {}  
        for subclass_name in subclass_dict.keys():  # iterate through node subclass names

            if (not subclass_name) or subclass_name == '':
                continue    # go to the next subclass name
            cal_event_obj_type = eval(subclass_name)     # e.g. eval('Page')
            # retrieve subclass instances
            subclass_object_qs = cal_event_obj_type.objects.select_related().filter(id__in=event_ids, visible=True) 
            # put subclass instances into lookup
            for subclass_obj in subclass_object_qs:  
                    evt_subclass_objects.update({ subclass_obj.id: subclass_obj })

        # Iterate through the nodes and, if subclass available, REPLACE with the appropriate 'subclass'
        #
        formatted_events = []
        for nd in calendar_events:
            # if subclass is available, replace the node with its subclass
            #formatted_events.append(evt_subclass_objects.get(nd.id, nd))
            subclass_obj = evt_subclass_objects.get(nd.id, None)
            if subclass_obj:
                formatted_node = subclass_obj
            else:
                formatted_node = nd

            if formatted_node.id in active_path_ids:
                formatted_node.active_path = True
            else:
                formatted_node.active_path = False

            if len(active_path_ids) > 0 and nd.id == active_path_ids[-1]:
                formatted_node.selected_node = True

            formatted_events.append(formatted_node)      # subclass not found, use the Node
        return formatted_events
    