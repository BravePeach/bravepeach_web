"""
This is sample setting file.
You can copy and use your local system or server.
For local, copy it to "local.py"
For stating server, copy it to "staging.py"
For service, copy it to "service.py"

Edit bravepeach/wsgi.py. Change setting for your purpose. Default is local.
"""

from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'SECRET KEY HERE'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True    # NEVER SET "True" IN SERVICE!!!!

ALLOWED_HOSTS = []  # add your ip address

INTERNAL_IPS = []    # add "127.0.0.1" when make local

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',      # DB Name
        'USER': '',      # DB User
        'PASSWORD': '',  # User PW
        'HOST': '',      # DB Host. Remain empty for localhost
        'PORT': '',      # DB Port. Remain empty for default port
    }
}

# AWS
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
