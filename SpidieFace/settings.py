"""
Django settings for SpidieFace project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djangotoolbox',
    'reports',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'SpidieFace.urls'

USE_X_FORWARDED_HOST = False

WSGI_APPLICATION = 'SpidieFace.wsgi.application'

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]
# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

## Note that HOST: localhost will not work as the docker containers use this host for communications
DATABASES = {
    'default': {
        'ENGINE' : 'django_mongodb_engine',
        'NAME': 'fjospidie',
        'HOST': os.environ['MONGO_HOST'],
        'PORT': os.environ['MONGO_PORT']
    }
}
INTERCEPT_REDIRECTS=True
HIDE_DJANGO_SQL=False

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

USE_I18N = True

USE_L10N = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/'
