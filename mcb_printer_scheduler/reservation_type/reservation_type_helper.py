from datetime import date
from reservation_type.models import ReservationType
"""
Given a particular day, choose the ReservationType that applies
"""

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
        
    return choose_reservation_type_by_date(selected_datetime)
    
def choose_reservation_type_by_date(selected_date):
    if selected_date is None:
        return None

    qset = ReservationType.objects.filter(is_active=True) 
    
    # (1)  Look for date specific reservation type
    # Is there an active reservation type for the given date?
    # (Should only be one of these, it is constrained by the admin)
    qset_date_specific = qset.filter(start_date__lte=selected_date\
                                    , end_date__gte=selected_date)
    if qset_date_specific.count() > 0:
        return qset_date_specific[0]
    
    # (2) Look for the default reservation type -- with no date range
    #
    qset_date_default = qset.filter(is_default=True\
                                , start_date__lte=selected_date\
                                    , end_date__gte=selected_date)
    if qset_date_specific.count() > 0:
        return qset_date_specific[0]
    
    opening_time = models.TimeField()
    closing_time = models.TimeField()

    time_block = models.IntegerField('minutes in a time block', default=20)
    
    scheduling_window_in_days = models.IntegerField('How many days in advance may a user schedule?', default=365)

    is_active = models.BooleanField(default=False)
    is_default = models.BooleanField(default=False)