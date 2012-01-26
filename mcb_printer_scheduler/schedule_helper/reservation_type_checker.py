from django.db.models.signals import post_save

def check_reservation_type(sender, **kwargs):
    """Make sure only one ReservationType object is active at once.
        - sender is a ReservationType object"""
    
    reservation_type_class = sender
    
    selected_rt = kwargs.get('instance', None)
    if selected_rt is None:
        return
    
    # temporarily disconnect the post_save signal
    post_save.disconnect(check_reservation_type, reservation_type_class)

    # update iso numbers
    selected_rt.day_iso_numbers = selected_rt.get_day_iso_numbers()
    selected_rt.save()
    
    if selected_rt.is_default:
        selected_rt.is_active = True
        selected_rt.save()
        # The last reservation type saved is 'is_default', 
        # mark all others as not 'is_default'
        for reservation_type in reservation_type_class.objects.exclude(id=selected_rt.id):
            if reservation_type.is_default:
                reservation_type.is_default = False
                reservation_type.is_active = False
                reservation_type.save()
    else:
        num_default = reservation_type_class.objects.filter(is_default=True).count()
        if num_default == 1:
            # only one active ReservationType, very good
            pass
        elif num_default == 0:
            # no ReservationType objects are active, 
            # make the last one saved active
            selected_rt.is_default = True
            selected_rt.is_active = True
            selected_rt.save()
        elif num_default > 1:
            # too many ReservationType objects are active, 
            # make the last active one saved the only active one
            cnt =0
            for rt in reservation_type_class.objects.filter(is_default=True).all().order_by('-last_update'):
                if cnt > 0:     # 1st one is left as active
                    rt.is_default = False
                    rt.is_active = False
                    rt.save()
                cnt+=1  
        
        
    post_save.connect(check_reservation_type, reservation_type_class)
    
    
    