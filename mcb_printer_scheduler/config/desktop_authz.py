# rprasad/123
# Django settings for mcb_printer_scheduler project.
import os
import sys
PROJECT_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(__file__), '../', '../'))
PIN_DIR = os.path.join(PROJECT_DIRECTORY, '../', 'Django-HU-Pin-Auth')

pths = (PIN_DIR, )
for p in pths:
    if os.path.isdir(p):
        sys.path.append(p)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Raman Prasad', 'raman_prasad@harvard.edu'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(PROJECT_DIRECTORY, 'db', 'printer.db3'), 
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_DIRECTORY, 'media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/poster-printer/media/'

STATIC_ROOT = os.path.join(PROJECT_DIRECTORY, 'collected_static_files/')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (os.path.join(PROJECT_DIRECTORY, 'static_site_files'),)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'o_st3i44&+7(xygp7%!!x(3$y+*f@#=qqe53orqv!c77lm1n@x'



ROOT_URLCONF =  'mcb_printer_scheduler.urls_test'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIRECTORY, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    #'hu_ldap_basic',
    #'hu_pin_auth',
    #'hu_authzproxy',
    'mcb_printer_scheduler.media_type',
    'mcb_printer_scheduler.poster_tube',
    'mcb_printer_scheduler.calendar_user',
    'mcb_printer_scheduler.calendar_event',
    'mcb_printer_scheduler.mcb_image_record',
    'mcb_printer_scheduler.reservation_type',
    'mcb_printer_scheduler.hu_authz_handler',
    'mcb_printer_scheduler.design_links',

)

LOGIN_URL = '/poster-printer/'

HU_PIN_LOGIN_APP_NAME = 'FAS_FCOR_MCB_GPPS_AUTHZ_DEV'   #'FAS_FCOR_MCB_GPPS_DEV'
HU_PIN_LOGIN_APP_NAMES = (HU_PIN_LOGIN_APP_NAME,) #'FAS_MCB_AUTH_DEV',)

SESSION_COOKIE_NAME = 'mcb_graphics_poster_printer_test'

AUTHENTICATION_BACKENDS = (   'django.contrib.auth.backends.ModelBackend'\
        ,'hu_authzproxy.hu_authz_pin_backend.HarvardAuthZProxyBackend' \
)

#LDAP_CUSTOMER_NAME = 'mcb'
#LDAP_CUSTOMER_PASSWORD = '*9xfJfWc' 
#LDAP_SERVER = 'ldaps://hu-ldap-test.harvard.edu'


GNUPG_HOME = '/Users/rprasad/mcb-git/Django-HU-Pin-Auth/test_files/gnupg_poster_printer'
GPG_PASSPHRASE = None

MCB_GRAPHICS_EMAIL = 'raman_prasad@harvard.edu' # 'mcbgraphics@fas.harvard.edu'



LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

POORMANS_DB_BACKUP_DIR = 'use for prod mysql backups'
