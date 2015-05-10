# -*- coding: utf-8 -*-
"""
Django settings for facesapi project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
from __future__ import unicode_literals
from datetime import timedelta

from django.utils.translation import ugettext_lazy

from faces.api.server_settings import DEBUG, SECRET_KEY, RAVEN_CONFIG, INSTALLED_APPS as SERVER_INSTALLED_APPS, \
    MIDDLEWARE_CLASSES as SERVER_MIDDLEWARE_CLASSES, DATABASES, ALLOWED_HOSTS, COMPRESS_PRECOMPILERS, \
    COMPRESS_OFFLINE, SERVER_EMAIL, EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_PORT, EMAIL_USE_TLS, \
    CACHES, GOOGLE_ANALYTICS_UA, SITE_URL, P24_API_TYPE, ENV, DEMO_URL, BROKER_URL, FACEBOOK_APP_ID, \
    FACEBOOK_APP_SECRET

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = (
                     'django_extensions',
                     'django.contrib.auth',
                     'django.contrib.contenttypes',
                     'django.contrib.sessions',
                     'django.contrib.messages',
                     'django.contrib.staticfiles',
                     'django.contrib.humanize',
                     'grappelli',
                     'django.contrib.admin',
                     'rest_framework',

                     'faces.api.apps.users',
                     'faces.api.apps.faces',
                     'faces.api.apps.images',
                     'faces.api.apps.products',

                     'bootstrapform',
                     'compressor',
                     'ckeditor',
                     'lineage',
                     'django_countries',
                     'easy_maps',
                     'post_office',
                     'statici18n',
                     'datetimewidget',
                     'sorl.thumbnail',
                     'dbbackup',
                     'djcelery',
                     'django_jenkins',
                 ) + SERVER_INSTALLED_APPS

MIDDLEWARE_CLASSES = (
                         # 'django.middleware.cache.UpdateCacheMiddleware',
                         'django.contrib.sessions.middleware.SessionMiddleware',
                         'django.middleware.locale.LocaleMiddleware',
                         'django.middleware.common.CommonMiddleware',
                         'django.middleware.csrf.CsrfViewMiddleware',
                         'django.contrib.auth.middleware.AuthenticationMiddleware',
                         # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
                         'django.contrib.messages.middleware.MessageMiddleware',
                         'django.middleware.clickjacking.XFrameOptionsMiddleware',
                         # 'django.middleware.cache.FetchFromCacheMiddleware',
                     ) + SERVER_MIDDLEWARE_CLASSES
if DEBUG:
    MIDDLEWARE_CLASSES += ('faces.lib.middlewares.ErrorHandlingMiddleware', )

ROOT_URLCONF = 'faces.api.urls'
WSGI_APPLICATION = 'faces.api.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/
LANGUAGE_CODE = 'pl'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'src', 'faces', 'api', 'locale'),
)

ugettext = lambda s: s
LANGUAGES = (
    ('pl', ugettext('Polish')),
    ('en', ugettext('English')),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "src", "static"),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

HOST_NAME = "http://faces.hern.as"

CASSETTES_DIR = os.path.join(BASE_DIR, 'src', 'faces', 'cassettes')

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
)

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}

COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter'
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)
COMPRESS_ENABLED = True
COMPRESS_OFFLINE_CONTEXT = {
    'STATIC_URL': STATIC_URL,
    'GOOGLE_ANALYTICS_UA': GOOGLE_ANALYTICS_UA
}

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_JQUERY_URL = STATIC_URL + 'bower_components/jquery/dist/jquery.min.js'
CKEDITOR_RESTRICT_BY_USER = True

if DEBUG:
    LOGGING = {
        'version': 1,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            }
        },
        'root': {
            'handlers': ['console'],
            'level': 'INFO'
        },
        'faces.api': {
            'handlers': ['console'],
            'level': 'INFO'
        },

        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        }
    }
SENTRY_AUTO_LOG_STACKS = True

ADMINS = (
    ('Bartosz Hernas', 'bartosz+facesapi@hernas.pl'),
    ('Michal Hernas', 'michal+facesapi@hernas.pl'),
)

AUTH_USER_MODEL = 'users.User'

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar_Full2': [
            ['Styles', 'Format', 'Bold', 'Italic', 'Underline', 'Strike', 'Align', 'SpellChecker', 'Undo', 'Redo'],
            ['Image', 'Flash', 'Table', 'HorizontalRule'],
            ['TextColor', 'BGColor'],
            ['Smiley', 'SpecialChar'], ['Source'],
        ],
        'toolbar': 'Full2',
        'height': 300,
        'width': 800,
    },
    'small': {
        'toolbar': 'Full',
        'height': 100,
        'width': 800,
    },
}

LOGIN_URL = 'admin:user:login'
LOGOUT_URL = 'admin:user:logout'
LOGIN_REDIRECT_URL = 'admin:index'

COUNTRIES_ONLY = {
    'PL': ugettext_lazy('Poland'),
    'DE': ugettext_lazy('Germany'),
}

EMAIL_BACKEND = 'post_office.EmailBackend'


# Backups
DBBACKUP_BACKUP_DIRECTORY = os.path.join(BASE_DIR, 'backups', 'api')

THUMBNAIL_PRESERVE_FORMAT = True

GYG_TOKEN = 'nJ57MkINKktDEGRP2lOzIP85K7I9pkuIhpwr2UWP5yludiUz'

FACES_SECRET = 'orghdugfd76%$$%67sf5sd$$45'

ECHO_NEST_API_KEY = "E8IOBG3UOIB2IF5HT"

MAIN_SITE_URL = 'https://faces.it'

GRAPPELLI_SWITCH_USER = True

CELERY_TIMEZONE = 'UTC'

# Face API

FACE_API_SUBSCRIPTION_KEY = "b93b9ef5a69b42e68a221041488db6c2"
FACE_API_PERSON_GROUP_ID = "ecomhack"

# Sphere API

SPHERE_API_CLIENT_ID = "cine9sknRb1S9YYWYTZcBl9S"
SPHERE_API_CLIENT_SECRET = "ZuumXEDaD6Uo8X57o4GTluuSbZFac1MV"
SPHERE_API_PROJECT_KEY = "ecomhack_faces"

# expires in 11.05.2015
SPHERE_API_ACCESS_TOKEN = "7N42tZpb9bGPnYycseU6ploMxPBlSaUo"

ZALANDO_API_CLIENT_NAME = "ecomhack_faces"

