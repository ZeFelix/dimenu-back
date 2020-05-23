"""
Django settings for cardapio project on Heroku. For more info, see:
https://github.com/heroku/heroku-django-template

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

###### Para uso com o sistema de recomendações ######
# import redis

import os
import dj_database_url
import django_heroku
from datetime import timedelta

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = "_$l7g-*oaob=$k8j@w=u%f3e0d5h0w-3-*d_u@3nyx=ud!@vm="
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', "_$l7g-*oaob=$k8j@w=u%f3e0d5h0w-3-*d_u@3nyx=ud!@vm=")

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True
DEBUG = bool(os.environ.get('DJANGO_DEBUG', True))

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # Disable Django's own staticfiles handling in favour of WhiteNoise, for
    # greater consistency between gunicorn and `./manage.py runserver`. See:
    # http://whitenoise.evans.io/en/stable/django.html#using-whitenoise-in-development
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'api',
    'storages',    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cardapio.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': DEBUG,
        },
    },
]

WSGI_APPLICATION = 'cardapio.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dimenu',
        'USER': 'postgres',
        'PASSWORD': 'joseph',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Change 'default' database configuration with $DATABASE_URL.
DATABASES['default'].update(dj_database_url.config(conn_max_age=500, ssl_require=True))

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


#configuração para permitir acesso de qualquer host
CORS_ORIGIN_ALLOW_ALL = True
ALLOWED_HOSTS = ['*']

#lita branca 
#CORS_ORIGIN_WHITELIST = ('*','google.com', 'hostname.example.com', 'http//:localhost:8000/', 'http//:localhost:3000/',  '10.42.0.1', '127.0.0.1:9000') 
 
#CORS_ALLOW_HEADERS = ['Origin','X-Requested-With', 'Content-Type','Accept','X-CSRFTOKEN','Authorization'] 
CORS_ALLOW_HEADERS = ( 
    'accept', 
    'accept-encoding', 
    'authorization', 
    'content-type', 
    'dnt', 
    'origin', 
    'user-agent', 
    'x-csrftoken', 
    'x-requested-with', 
) 
CORS_ALLOW_METHODS = ( 
    'DELETE', 
    'GET', 
    'OPTIONS', 
    'PATCH', 
    'POST', 
    'PUT', 
) 
#CORS_ALLOW_METHODS = ['POST','GET','DELETE','OPTIONS','PUT'] 
CORS_ALLOW_CREDENTIALS = True 


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, 'static'),
]

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
#STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Activate Django-Heroku.
django_heroku.settings(locals())

#configuração para midias
#MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

#configuração global do prefixo do token
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=8),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),

    'AUTH_HEADER_TYPES': ('Bearer',),
    
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(hours=8),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

#aws amazon s3 configurações para armazenamento no aws amazon
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
AWS_S3_REGION_NAME = 'sa-east-1' 
AWS_STORAGE_BUCKET_NAME = 'digimenu-media'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'media'

MEDIA_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)

MEDIAFILES_LOCATION = 'media'

#Classe com confguração para as medias
DEFAULT_FILE_STORAGE = 'cardapio.storage_backends.MediaStorage'


####### Configuração do Redis #######
# Para uso com o sistema de recomendação

# REDIS_HOST = 'localhost'
# REDIS_PORT = 6379
# REDIS_DB = 0
