from calendar_event.models import CalendarEvent

class ConflictChecker:
    """
    proposed_timeslot: requires start_datetime and end_datetime objects
    """
    @staticmethod
    def check_for_conflicts(proposed_timeslot, calendar_events):
        
# 1- check if previous session ended during the new session 
#   
#       |           |
#       |et   et   e|t     
#       |           |
#         
for sts in ResourceReservation.objects.filter(resource=resource
                           , end_time__gt=start_time
                           , end_time__lte=end_time).exclude(id_md5=reservation_to_edit_id_md5):

    #msg('num slots used - 1: %s' % num_slots_used)
    if not sts.id in reservations_checked:
        reservations_checked.append(sts.id)
        num_slots_used += sts.reserved_slots

# 2- check if a previous session started during the new session 
#   
#       |            |
#      s|t   st    st|     
#       |           |
#         
for sts in ResourceReservation.objects.filter(resource=resource
                            , start_time__gte=start_time
                            , start_time__lt=end_time).exclude(id_md5=reservation_to_edit_id_md5):
    #msg('num slots used - 2: %s' % num_slots_used)
    if not sts.id in reservations_checked:
        reservations_checked.append(sts.id)
        num_slots_used += sts.reserved_slots

# 3- check if a previous session "encompassed" the new session 
#   (e.g. started before or at same time AND ended after or at same time) 
#
#   
#       |            |
#     st|            |et     
#       |           |
#         
for sts in ResourceReservation.objects.filter(resource=resource
                            , start_time__lte=start_time
                            , end_time__gte=end_time).exclude(id_md5=reservation_to_edit_id_md5):
   #msg('num slots used - 3: %s' % num_slots_used)
   if not sts.id in reservations_checked:
       reservations_checked.append(sts.id)
       num_slots_used += sts.reserved_slots
