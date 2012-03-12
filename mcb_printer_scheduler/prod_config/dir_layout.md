# 3/12/2012

## Layout for deployment to mcbweb.unix.fas.harvard.edu 

* Django apps via github
    * /home/p/r/prasad/webapps/django/MCB-Graphics-Printer-Scheduler
    * /home/p/r/prasad/webapps/django/mcb_lib/Django-HU-Pin-Auth
    x* /home/p/r/prasad/webapps/django/mcb_lib/CMS-Basics
    x* /home/p/r/prasad/webapps/django/mcb_lib/django-ckeditor
    x* /home/p/r/prasad/webapps/django/mcb_lib/Poor-Mans-Tag

* Static and Media Files
    * /var/www/poster_printer/media
    * /var/www/poster_printer/collected_static

## django settings
* updates for db, file locations, etc.

## apache/mod_wsgi
* /etc/apache2/sites-available/mcb_graphics_scheduler

/etc/apache2/sites-available

* upload file dir

http://mcbweb.unix.fas.harvard.edu/static/media/tutors/Nancy_Kleckner_2.jpg


/etc/apache2/sites-available