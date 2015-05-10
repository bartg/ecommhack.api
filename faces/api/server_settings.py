DEBUG = True

P24_API_TYPE = "sandbox"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'zgay=8g#@#=dm7gfk*l-b*ir_o4qun$u_-5x2fn+r0&e1&owum'


# Set your DSN value
RAVEN_CONFIG = {}

# Application definition

INSTALLED_APPS = ()

MIDDLEWARE_CLASSES = ()

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'faceslocal',
        'USER': 'faceslocal',
        'PASSWORD': 'm3V8A96XNwfx5V,',
        'HOST': 'localhost',
        'PORT': '',
    }
}

ALLOWED_HOSTS = ['.*']
SITE_URL = 'http://localhost:8082/'
DEMO_URL = "demo.localhost:8081"

COMPRESS_PRECOMPILERS = (
    ('text/less', '/webapps/faceslocal/node_modules/less/bin/lessc {infile} {outfile}'),
)
COMPRESS_OFFLINE = False

#SERVER_EMAIL = "donotreply@localhost"
SERVER_EMAIL = "donotreply@faces.pl"
EMAIL_HOST = 'smtp.zenbox.pl'
EMAIL_HOST_USER = 'donotreply@faces.pl'
EMAIL_HOST_PASSWORD = '38Gg/Fsm8azLnJfBDZmBT4oy+MbmEb#aVNLkCEw6LH#s;rDibX'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

GOOGLE_ANALYTICS_UA = ""
ENV = "development"

BROKER_URL = 'amqp://faceslocal:9gfZ5zM9TrJ7St:@localhost:5672//faceslocal'

FACEBOOK_APP_ID = '826201467468902'
FACEBOOK_APP_SECRET = '1f3538643fa01d06385d168b91793011'
