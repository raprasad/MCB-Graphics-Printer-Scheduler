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

    if selected_rt.is_active:
        # The last reservation type saved is 'active', 
        # mark all others as inactive
        for reservation_type in reservation_type_class.objects.exclude(id=selected_rt.id):
            reservation_type.is_active = False
            reservation_type.save()
    else:
        num_active = reservation_type_class.objects.filter(is_active=True).count()
        if num_active == 1:
            # only one active ReservationType, very good
            pass
        elif num_active == 0:
            # no ReservationType objects are active, 
            # make the last one saved active
            instance.is_active = True
            instance.save()
        elif num_active > 1:
            # too many ReservationType objects are active, 
            # make the last active one saved the only active one
            cnt =0
            for rt in reservation_type_class.objects.filter(is_active=True).all().order_by('-last_update'):
                if cnt > 0:     # 1st one is left as active
                    rt.is_active = False
                    rt.save()
                cnt+=1  
        
    
    
    