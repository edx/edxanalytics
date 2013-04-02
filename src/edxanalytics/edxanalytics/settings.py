# Django settings for edxanalytics project.

#### djanalytics-specific settings

import datetime
import os.path
import path
import sys

from pkg_resources import resource_filename

DJ_REQUIRED_APPS = ( 'djeventstream.httphandler',
    'djcelery',
    'south',
    'djanalytics.core',
    'djanalytics.modulefs',
#    'modules',
)

# Types of parameters that queries and views can take. 
# This is not properly used yet. 
DJANALYTICS_PARAMETERS = ['user', 'filename']
DJFS = { 'type' : 'osfs',
         'directory_root' : '/tmp/djfsmodule',
         'url_root' : 'file:///tmp/'
       }


TIME_BETWEEN_DATA_REGENERATION = datetime.timedelta(minutes=1)

INSTALLED_ANALYTICS_MODULES = () #'modules.testmodule',)
INSTALLED_ANALYTICS_MODULES = ('modules.course_stats', 
                               'modules.mixpanel', 
                               'modules.event_count', 
                               'modules.student_course_stats', 
                               'modules.user_stats')

#Initialize celery
import djcelery
djcelery.setup_loader()

SNS_SUBSCRIPTIONS = []

import django.contrib.auth.decorators
DJA_AUTH = { '.*' : django.contrib.auth.decorators.login_required } 

#### Remaining settings

LOGIN_REDIRECT_URL = "/"
MAKO_MODULE_DIR = '../../compiled_templates' # TODO: Use pkg_resources.resource_filename
MAKO_TEMPLATES = {'main': 'templates'}
DUMMY_MODE = False # Slight TODO: This send back fake data from queries for off-line development
# DATABASE_ROUTERS = ['djanalytics.djanalytics.router.DatabaseRouter'] # TODO
PROTECTED_DATA_ROOT = os.path.abspath("../../protected_data") # TODO: Use pkg_resources.resource_filename

#### MITx settings

IMPORT_MITX_MODULES = False
if IMPORT_MITX_MODULES:
    BASE_DIR = os.path.abspath(os.path.join(__file__, "..", "..", ".."))
    ROOT_PATH = path.path(__file__).dirname()
    REPO_PATH = ROOT_PATH.dirname()
    ENV_ROOT = REPO_PATH.dirname()

    MITX_PATH = os.path.abspath("../../../mitx/")
    DJANGOAPPS_PATH = "{0}/{1}/{2}".format(MITX_PATH, "lms", "djangoapps")
    LMS_LIB_PATH = "{0}/{1}/{2}".format(MITX_PATH, "lms", "lib")
    COMMON_PATH = "{0}/{1}/{2}".format(MITX_PATH, "common", "djangoapps")
    MITX_LIB_PATHS = [MITX_PATH, DJANGOAPPS_PATH, LMS_LIB_PATH, COMMON_PATH]
    sys.path += MITX_LIB_PATHS

    IMPORT_GIT_MODULES = False
    GIT_CLONE_URL = "git@github.com:MITx/{0}.git"
    COURSE_FILE_PATH = os.path.abspath(os.path.join(ENV_ROOT, "xml_data"))
    COURSE_CONFIG_PATH = os.path.abspath(os.path.join(REPO_PATH, "course_listings.json"))

    #Needed for MITX imports to work
    from mitx_settings import *

    MITX_ROOT_URL = ''
else:
    # TODO: Use resource_filename
    MITX_LIBRARY_PATH = os.path.abspath("mitx_libraries")
    sys.path.append(MITX_LIBRARY_PATH)

DATABASE_ROUTERS = ['edxanalytics.mitxrouter.MITxRouter']

#### Standard settings

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': { 
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '../../localdb.sql', # TODO: Use pkg_resources.resource_filename
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }, 
    'remote': { ## Small, local read/write DB for things like settings, cron tasks, etc. 
         'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
         'NAME': '../../../db/mitx.db', # TODO: Use pkg_resources.resource_filename
         'USER': '',                      # Not used with sqlite3.
         'PASSWORD': '',                  # Not used with sqlite3.
         'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
         'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
     }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'analytics-experiments'
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

import os.path

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.abspath("../css_js_src"), # TODO: Use pkg_resources.resource_filename
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'znl&amp;ht2r^_%ydx^uk&amp;*960xk7%=#gv5g)!7p81pe_$ph@lq+_4'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'edxanalytics.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'edxanalytics.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    "templates"
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
) + DJ_REQUIRED_APPS


syslog_format = ("[%(name)s][env:{logging_env}] %(levelname)s "
                 "[{hostname}  %(process)d] [%(filename)s:%(lineno)d] "
                 "- %(message)s").format(
    logging_env="", hostname="")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s %(levelname)s %(process)d '
                      '[%(name)s] %(filename)s:%(lineno)d - %(message)s',
            },
        'syslog_format': {'format': syslog_format},
        'raw': {'format': '%(message)s'},
        },
    'handlers': {
        'console': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'stream': sys.stdout,
            },
        },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
            },
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
        }
}