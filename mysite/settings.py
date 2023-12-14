"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 3.2.18.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
from decouple import config, Csv
import dj_database_url
from datetime import timedelta
# Build paths inside the project like this: BASE_DIR / 'subdir'.
#BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY',default="django-insecure-su=)@xq4w2v(%qiz)9&ir-92w&ac0hq=$bs#wgf9&3lmm^3i&i")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ["*"]

MARKDOWNIFY_STRIP = False

MARKDOWNIFY = {
    "default": {
        "WHITELIST_TAGS": [
            'a','blockquote','code','em','h1','h2','h3','h4','h5','h6','h7','li','ol','p','strong','ul'
        ]
    }
}


# Application definition

INSTALLED_APPS = [
    'restser',
    'cobrox',
    'user',
    'markdownify',
    'crispy_forms',
    'widget_tweaks',
    'django.contrib.humanize',
    'django.contrib.postgres',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'simple_history',
    'storages',
    'rest_framework.authtoken',
    'wsfacturae',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
    'django_currentuser.middleware.ThreadLocalUserMiddleware',
]

ROOT_URLCONF = 'mysite.urls'
CRISPY_TEMPLATE_PACK = 'bootstrap4'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL', default="postgres://postgres:%s@localhost:5432/micobroxdb" % r"admin")
    )
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': '10000/hour',
    },
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'DATETIME_INPUT_FORMATS': [
        '%d/%m/%Y %H:%M:%S'
    ],
}

# Configurar la duración de tiempo para el token
REST_FRAMEWORK_TOKEN_DURATION = timedelta(hours=24)

WS_ENTORNO_FIRMA = '002'
WS_ENTORNO = '001'
WS_USER_AGENT = 'user_agent'
WS_USER = 'user'
WS_USER_PWD = 'pwd'
WS_TOKEN_VIGENCIA = 24
WS_CONTENT_TYPE_JSON = 'application/JSON'
WS_CONTENT_TYPE_APP_URLENCODED = 'application/x-www-form-urlencoded'



NUM_RECS_BY_PAG = 25
# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/El_Salvador'

USE_I18N = True

USE_L10N = False
DATE_FORMAT = "d/m/Y"
DATETIME_FORMAT = 'd/m/Y H:i:s'

USE_TZ = False

#STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'mysite/static'),
]

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
DEFAULT_FILE_STORAGE = 'mysite.storage_backends.MediaStorage'

LOGIN_URL = '/user/login'
LOGIN_ERROR_URL = '/user/login'
ROOT_URLCONF = 'mysite.urls'
LOGIN_REDIRECT_URL = 'cobrox:index'
LOGOUT_REDIRECT_URL = 'user:login'

MEDIA_URL =  '/media/'
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

DATETIME_INPUT_FORMATS = ['%Y-%m-%d %H:%M:%S']
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
