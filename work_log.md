# 1/24/2012 - initial setup
* created project + settings file

# 1/25/2012 - 7:33pm to 10:01pm, 10:30pm to 12:20am
* basic calendar user set up in admin 
* reservation models set up
* model for minutes/days
* reservation type in
* started some tests
* Next: algorithm to check for conflicts
	* forms for
		* user entered reservation
		* admin entered reservation (for user)
		* admin edit a reservation
		* admin entered full day message
		* admin entered regular message
* Timed Notice Event - across top of calendar.  e.g. show 'Closed until January 2nd' message

# 1/26/2012 - 9:45am to 11:45am
* basic template, then scheduling form
* adjusted reservation_type

# 1/27/2012 - 10:15am (new haven) 1:28pm	(including fielding many work emails)
* see if we can't get the month view going:)
* basic month view working with test event

# 1/30/2012 - 9:30am to 10:00am / 4:00pm to 4:15pm
* script to make random reservations
* adjusted the filter times for viewing the monthly calendar

# 2/6/2012 - 9:30am to 11:00am
* work on sign up page

# 2/7/2012 - 1:15pm to 5:35pm (coffee break 3:14 to 4:50)
* scheduling - avail slots
* conflict checking, slotmaking, etc working!!

# 2/8/2012 - 11:15am to 4:30pm
* scheduling sign up form
* basic sign-up working

# 2/8/2012 - 8:00pm to 9:00pm
* reading django docs re: media and static files

# 2/9/2012 - 9:45am to 3:00pm
* implement static/media
*FIXED(i) time slot maker, make sure time has not passed e.g, if signing up that day

# 2/9/2012 - 7:45pm to 10:15pm (multiple zahra stops)
* logout page, username in header
* redo display names
* substitute cal-events for subclasses
* cancellation added for users

# 2/13/2012 - 1:50pm to 4:05pm (css fixup)
* css fixup on the monthly calendar

# 2/28/2012 - 11:14am to 12:15pm, 3:00pm to 5:00pm
* PIN login working
* Adjusted signup form for 33-digit code and lab name

# 2/29/2012 - 12:00pm to 3:00pm
* allow cancel for admin (misplaced if statement)
* remove end time from dropdown, reservation confirmation, and cancel pags
* added basic history page
* started rewriting scheduled banner.
* Add separate form for 33-digit code: http://digitalbush.com/projects/masked-input-plugin/
370-31560-6600-000775-600200-0000-44733

# 3/5/2012 - 3:30pm to 5:00pm
* admin form to sign up for anyone
    * basics are working

# 3/6/2012 - 9:40am to 11:15pm, 1:00pm to 2:07pm, 2:22pm to 3:05pm, 3:30pm to 5:00pm
* blackout form
    x*fixed x- cancel is via admin
    x* need time chooser for start/end times
    x* basic start/end times there
    x* need to jquery/ajax end time choices
    x* right col reservation diff
    x* monthly col display
x* blackout success page
x* top menu
x* cancel blackout date
x* signup for another user: add jquery to update email, phone, lab if user changes
x* blackout slots
* blackout days
    x* basic form
    x* right cal view
    * month cal view
-> redo Blackout Days
    - limit to 10 day length
    - for each day, make a separate CalendarFullDayMessage object
     

#----------------    

* limit scheduling ahead by 1year
* too many cancels on same day, give warning
* too many reservations same day, give warning



> one time slot per poster, up to 4 slots ok, 5 or more forget it
> plan ahead time 
> if less than 3 hours advance, email notice, please notify mcb graphics
> billing code 8260 default; validate it?
> no lab name
> reservation type with calendar dates that overrides defaults

