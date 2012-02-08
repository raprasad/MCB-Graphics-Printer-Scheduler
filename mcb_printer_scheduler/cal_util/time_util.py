import datetime

def get_next_month(date_obj):
    if date_obj is None:
        return None
        
    if date_obj.month == 12:
        return datetime.date(date_obj.year+1, 1, 1)
    else:
        return datetime.date(date_obj.year, date_obj.month+1, 1)

def get_previous_month(date_obj):
    if date_obj is None:
        return None

    if date_obj.month == 1:
        return datetime.date(date_obj.year-1, 12, 1)
    else:
        return datetime.date(date_obj.year, date_obj.month-1, 1)
