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
x* blackout days
    x* basic form
    x* right cal view

# 3/7/2012 - 6:45am to 7:28am, 9:20am - 11:45am, 2:45pm to 5:00pm
* local pin test
    x* /etc/apache2/httpd.conf
    x* RedirectMatch poster-printer/(.*) http://127.0.0.1:8000/poster-printer/$1
x* redo blackout days
	x* month cal view
(i)* for confirmation, retrieve message_group and iterate through all the blackout days
x* sign up as another user, add note field. for administrator: show note in monthly cal and in history
x* re-order reservation type to take in restrictive dates and non-default ReservationType first

# 3/8/2012 - 1:00pm to 3:30pm
*x blackout day group bg coloring, success message
* right col reservations, check off 'slot is available' work, allow 'double-booking'  
    * is slot is available, don't show on calendar but show in the history
* form for banner messages
* less than 3 hours, email to mcb graphics + msg to user
x* thumbnail of each poster -- img upload with note -- name images with hash
    x* upload screenshot, will be .png, change size to 500px wide
        x* allow multiple screenshots with names
	x* Note: for image resizing, use post_save functions            

# 3/9/2012 - prod. directory layout - 12:38pm to 3:00pm
* created "/Users/rprasad/webapps/django/mcb_lib"
* passphrase - gitmove
* git readonly:
* git full - scheduler:
    /home/p/r/prasad/webapps/django/MCB-Graphics-Printer-Scheduler

# 3/10/2012 - prod move - 9:30am to 12pm, 1pm to 5:50pm
* prepping prod file + prod directories with files
* initial set-up working

# 3/11/2012 - last minute warning - 9:15am to 10am

# 3/20/2012 - - 2:55pm to 3:39pm (zahra hospital)
x* monthly cal: remove day links unless person is signed in
x* move last signup time to 5:20 from 5:40 (last end time is 5:40)
* **form to adjust reservation type for a single day: 3 checkboxes with times available
* last minute reservation; remove online note and send email instead
x* monthly cal: black out times, display end time
* redo signup success page based on RH notes on print out
x* calendar login button alignment
x* "questions" button alignment
x* footer reduce font of timestamp and remove "(...)" 
x* right col listings, add day of week, e.g., "Thursday"
x* right col listings, change color of most recent signup from yellow to shade of green
* add link to fas logos ,etc
* add link to PDF download on current site
* when admin logged in, link to django admin
** mark reservation as allow signup for this time 

# 3/22/2012 - 11:00am to 3:02pm
x* add link to fas logos ,etc
x* add link to PDF download on current site
x* last minute reservation; remove online note and send email instead
x* redo signup success page based on RH notes on print out
x* when admin logged in, link to django admin
x* move mcbgraphics@fas.harvard.edu to a config variable

# 3/23/2012 - 9:30am to 11:00am, 11:40am to 1:30pm
x** mark reservation as allow signup for this time 
    x* model change
    x* month view
    x* right col view 
    x* conflict checking
    x* right col as form
**form to adjust reservation type for a single day: 3 checkboxes with times available
    x* set menu (10:40am)
    x* show current time span
    x* make form
    x    * 3 check boxes - 1 required
    x * 3 checkboxes:  9:00am to 12pm, 12pm to 6pm (default), 6pm to 8:40pm
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

