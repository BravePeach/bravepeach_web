"""
Django settings for bravepeach project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""
import os
import json

from django.core.management.utils import get_random_secret_key

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOCAL_SETTINGS = json.loads(open(os.path.join(BASE_DIR, "settings.json")).read())

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = LOCAL_SETTINGS["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = LOCAL_SETTINGS["DEBUG"]   # NEVER SET "True" IN SERVICE!!!!

ALLOWED_HOSTS = LOCAL_SETTINGS["ALLOWED_HOSTS"]     # add your ip address

INTERNAL_IPS = LOCAL_SETTINGS["INTERNAL_IPS"]   # add "127.0.0.1" when make local


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'debug_toolbar',
    'django_extensions',
    'django_mysql',
    'storages',
    'widget_tweaks',
    'static_precompiler',
    'django_user_agents',
    'redactor',
    'mathfilters',
    'social_django',
    'channels',
    'webapp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'bravepeach.middleware.UserAgentMiddleware',
]

ROOT_URLCONF = 'bravepeach.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'webapp/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'bravepeach.wsgi.application'

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = LOCAL_SETTINGS["DATABASES"]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'static_precompiler.finders.StaticPrecompilerFinder',
)

HASHID_FIELD_SALT = get_random_secret_key()

# Login info

# LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'

# Email backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = LOCAL_SETTINGS['EMAIL_HOST_USER']
EMAIL_HOST_USER = LOCAL_SETTINGS['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = LOCAL_SETTINGS['EMAIL_HOST_PASSWORD']

# Media
# MEDIA_ROOT = os.path.join(BASE_DIR,'media/')
AWS_S3_CUSTOM_DOMAIN = 'di6a2p2igrt9l.cloudfront.net'   # cdn.bravepeach.com after SSL
MEDIAFILES_LOCATION = 'media'
MEDIA_URL = "http://{domain}/{media}/".format(domain=AWS_S3_CUSTOM_DOMAIN, media=MEDIAFILES_LOCATION)
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
CONTENT_TYPES = ['image']
MAX_UPLOAD_SIZE = '5242880'     # 5M
# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 5242880
# 100MB 104857600
# 250MB - 214958080
# 500MB - 429916160

# AWS
AWS_STORAGE_BUCKET_NAME = 'bravestatics'
AWS_ACCESS_KEY_ID = LOCAL_SETTINGS["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = LOCAL_SETTINGS["AWS_SECRET_ACCESS_KEY"]

# For Deploy
APT_PACKAGE_LIST = ("git", "build-essential", "python3-dev", "python3-pip",
                    "libmysqlclient-dev", "libssl-dev", "libffi-dev",
                    )

# Session
# SESSION_COOKIE_AGE = 60*60  # 60min. After that, auto logout
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # browser-length session

# wysiwyg-redactor
# https://pypi.python.org/pypi/django-wysiwyg-redactor
REDACTOR_OPTIONS = {'lang': 'ko'}
REDACTOR_UPLOAD = 'uploads/'
REDACTOR_AUTH_DECORATOR = 'django.contrib.auth.decorators.login_required'

SOCIAL_AUTH_URL_NAMESPACE = 'social'

# FB Login
SOCIAL_AUTH_FACEBOOK_KEY = LOCAL_SETTINGS['FB_KEY']
SOCIAL_AUTH_FACEBOOK_SECRET = LOCAL_SETTINGS['FB_SECRET']
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': "id, name, first_name, last_name, gender, picture, age_range"
}

# Google Login
SOCIAL_AUTH_GOOGLE_API_KEY = LOCAL_SETTINGS['GGL_API']
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = LOCAL_SETTINGS['GGL_KEY']
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = LOCAL_SETTINGS['GGL_SECRET']

# Cert. email
ENCRYPT_KEY = LOCAL_SETTINGS["ENCRYPT_KEY"]

# Chatting
CHANNEL_LAYERS = {
    'default': {
        "BACKEND": 'asgi_redis.RedisChannelLayer',
        "CONFIG": {
            "hosts": [(LOCAL_SETTINGS["REDIS_HOST"], 6379)],
        },
        "ROUTING": "bravepeach.routing.channel_routing",
    }
}

from django.conf import settings

NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS = getattr(settings, 'NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS', True)

MSG_TYPE_MESSAGE = 0  # For standard messages
MSG_TYPE_WARNING = 1  # For yellow messages
MSG_TYPE_ALERT = 2  # For red & dangerous alerts
MSG_TYPE_MUTED = 3  # For just OK information that doesn't bother users
MSG_TYPE_ENTER = 4  # For just OK information that doesn't bother users
MSG_TYPE_LEAVE = 5  # For just OK information that doesn't bother users

MESSAGE_TYPES_CHOICES = getattr(settings, 'MESSAGE_TYPES_CHOICES', (
    (MSG_TYPE_MESSAGE, 'MESSAGE'),
    (MSG_TYPE_WARNING, 'WARNING'),
    (MSG_TYPE_ALERT, 'ALERT'),
    (MSG_TYPE_MUTED, 'MUTED'),
    (MSG_TYPE_ENTER, 'ENTER'),
    (MSG_TYPE_LEAVE, 'LEAVE'))
                                )

MESSAGE_TYPES_LIST = getattr(settings, 'MESSAGE_TYPES_LIST',
                             [MSG_TYPE_MESSAGE,
                              MSG_TYPE_WARNING,
                              MSG_TYPE_ALERT,
                              MSG_TYPE_MUTED,
                              MSG_TYPE_ENTER,
                              MSG_TYPE_LEAVE]
                             )
