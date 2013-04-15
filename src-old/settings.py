# Django settings for src project.

INSTALLED_ANALYTICS_MODULES = ('course_stats', 'mixpanel', 'page_count', 'student_course_stats', 'user_stats')

LOG_READ_DIRECTORY = "../../analytics-logs/"
LOG_POST_URL = "http://127.0.0.1:9022/event"

MODULE_RESOURCE_STATIC = os.path.join(ENV_ROOT,'resource')

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'mitxmako.middleware.MakoMiddleware',
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    BASE_DIR,
    str(os.path.abspath(REPO_PATH / 'templates/')),
    str(os.path.abspath(REPO_PATH / 'src/templates/')),
)

#Append these internal paths in order to load celery tasks properly
MODULE_DIR = "edxmodules"
sys.path.append(str(ROOT_PATH / MODULE_DIR ))

INSTALLED_APPS = (
    'dashboard',
    'edxmodules',
    'mitxmako',
    'frontend',
)

#Make each analytics module its own installed app
INSTALLED_APPS += INSTALLED_ANALYTICS_MODULES

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.

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


DIRECTORIES_TO_READ = []

BROKER_URL = 'redis://localhost:6379/0'
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_TASK_RESULT_EXPIRES = 60 * 60 #1 hour

STATIC_ROOT = os.path.abspath(REPO_PATH / "staticfiles")
NGINX_PROTECTED_DATA_URL = "/protected_data/"

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'
PROTECTED_DATA_URL = '/data/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.abspath(REPO_PATH / 'css_js_src/'),
)

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

PIPELINE_JS = {
    'util' : {
        'source_filenames': [
            'js/jquery-1.9.1.js',
            'js/json2.js',
            'js/underscore.js',
            'js/backbone.js',
            'js/backbone.validations.js'
            'js/jquery.cookie.js',
            'js/bootstrap.js',
            'js/jquery-ui-1.10.2.custom.js',
            'js/jquery.flot.patched-multi.js',
            'js/jquery.flot.tooltip.js',
            'js/jquery.flot.axislabels.js',
            ],
        'output_filename': 'js/util.js',
        },
    'new_dashboard' : {
        'source_filenames': [
            'js/new_dashboard/load_analytics.js'
            ],
        'output_filename': 'js/new_dashboard.js',
        },
}

PIPELINE_CSS = {
    'bootstrap': {
        'source_filenames': [
            'css/bootstrap.css',
            'css/bootstrap-responsive.css',
            'css/bootstrap-extensions.css',
            ],
        'output_filename': 'css/bootstrap.css',
        },
    'util_css' : {
        'source_filenames': [
            'css/jquery-ui-1.10.2.custom.css',
            ],
        'output_filename': 'css/util_css.css',
    }
}

PIPELINE_DISABLE_WRAPPER = True
PIPELINE_YUI_BINARY = "yui-compressor"

PIPELINE_CSS_COMPRESSOR = None
PIPELINE_JS_COMPRESSOR = None

PIPELINE_COMPILE_INPLACE = True
PIPELINE = True

CELERY_IMPORTS = ()
for analytics_module in INSTALLED_ANALYTICS_MODULES:
    module_name = "{0}.{1}.{2}".format(MODULE_DIR,analytics_module,"tasks")
    try:
        imp.find_module(module_name)
        CELERY_IMPORTS += (module_name,)
    except:
        pass


override_settings = os.path.join(BASE_DIR, "override_settings.py")
if os.path.isfile(override_settings):
    execfile(override_settings)
