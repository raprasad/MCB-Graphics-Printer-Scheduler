import calendar
from datetime import datetime
from platform import python_version

def fill_in_days(week_lst, is_first_week=False):
    """The input week may have "None" instead of Date objects.  If None appears, fill it in with days from the previous month, or next month
    
    1st week example:
        [None, None, datetime.date(11, 4, 1), datetime.date(11, 4, 2), datetime.date(11, 4, 3), datetime.date(11, 4, 4), datetime.date(11, 4, 5)]
    
    last week example: 
        [datetime.date(11, 4, 27), datetime.date(11, 4, 28), datetime.date(11, 4, 29), datetime.date(11, 4, 30), None, None, None]
        
    for pre-python 2.4
    """
    day_increment = 1
    if is_first_week:       
        # the first week is reversed since it can start with 'None'
        week_lst.reverse()
        day_increment = -1
    last_day = None
    fmt_week = []
    
    for idx, d in enumerate(week_lst):
        if d is None and last_day is not None:
            d = last_day + datetime.timedelta(days=day_increment)
        fmt_week.append(d)
        last_day = d

    if is_first_week: 
        fmt_week.reverse()

    return fmt_week


def get_calendar_weeks(date_obj):
    """Given a selected month, build a calendar with events
    
        Input: year, month (from selected_day)
       Output: A list of the weeks. Each week is a list of seven datetime.date objects.
    """
    if python_version()[:3] in ['2.3', '2.4']:
        pass
    else:           
        # For python 2.5 or higher, use built-in "monthdatescalendar" method
        cal = calendar.Calendar(calendar.SUNDAY)        # start the day of the week on sunday
        # a list of the weeks. Each week is a list of seven datetime.date objects.
        return cal.monthdatescalendar(date_obj.year, date_obj.month)   
       
        return cal_weeks        
        
    # built lists of datetime objects using older python
    calendar.setfirstweekday(calendar.SUNDAY)       # set sunday to first day of week
    week_lists = calendar.monthcalendar(date_obj.year, date_obj.month)  #   pull array of arrays
    cal_weeks = []
    for idx, wk in enumerate(week_lists):
        wk = map(lambda day_num: date(year=date_obj.year, month=date_obj.month, day=day_num), wk)
        cal_weeks.append(wk)
     
    cal_weeks[0] = fill_in_days(cal_weeks[0], is_first_week=True)
    cal_weeks[-1] = fill_in_days(cal_weeks[-1], is_first_week=False)
    
    return cal_weeks
