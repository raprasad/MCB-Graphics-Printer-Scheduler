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

# 1/30/2012 - 9:30 to 10:00am / 4 to 4:15
* script to make random reservations
* adjusted the filter times for viewing the monthly calendar

# 2/6/2012 - 9:30am to 11:00
* work on sign up page

# 2/7/2012 - 1:15pm to 5:35pm (coffee break 3:14 to 4:50)
* scheduling - avail slots
* conflict checking, slotmaking, etc working!!

# 2/8/2012 - 11:15am to 4:30pm
* scheduling sign up form
* basic sign-up working

# 2/8/2012 - 8pm to 9pm
* reading django docs re: media and static files

# 2/9/2012 - 9:45am to 3pm
* implement static/media
*FIXED(i) time slot maker, make sure time has not passed e.g, if signing up that day

(i) ScheduledBannerMessage should *not* be a CalendarEvent
* add cancel for users.
* add 'edit' for admin?
* too many cancels on same day, give warning
* too many reservations same day, give warning
* view my reservations



> one time slot per poster, up to 4 slots ok, 5 or more forget it
> plan ahead time 
> if less than 3 hours advance, email notice, please notify mcb graphics
> billing code 8260 default; validate it?
> no lab name
> reservation type with calendar dates that overrides defaults

