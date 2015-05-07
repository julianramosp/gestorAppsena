"""
Django settings for gestorApp project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SETTINGS_DIR = os.path.dirname(__file__)

PROJECT_PATH = os.path.join(SETTINGS_DIR, os.pardir)
PROJECT_PATH = os.path.abspath(PROJECT_PATH)

# Incluir Configuracion BASE DE DATOS

# import databases

# DATABASES = databases.db()



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9+()f6f*s^81ocqrclp5b4alay%&^b^!)bvb=rftm^)x6ntx@c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'web',
    'easy_pdf',
    'model_report',
    'modulo3',
    'geraldo',
    'xhtml2pdf',
    'import_export',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

ROOT_URLCONF = 'gestorApp.urls'

WSGI_APPLICATION = 'gestorApp.wsgi.application'

# Fecha creado: 12/09/2014
# Proposito: Especificar el dierctorio static en el sistema

STATICFILES_DIRS = (
    os.path.join(BASE_DIR,'static'),
)




# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'gestorapp',
        'HOST': 'localhost',
        'PORT': 5432,
        #'USER': 'sena',
        'USER': 'postgres',
        #'PASSWORD': 'admin'
		'PASSWORD': 'granados'
    }
}


DATABASES['default'] =  dj_database_url.config()


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
# Fecha actualizado: 03/09/2014
# Cambio realizado: Cambiar lenguaje de la interfaz
# Fecha actualizado: 12/09/2014
# Cambio realizado: Interpretacion idioma y zona horaria, Ln 91,94. Desactivacion USE_TZ en False, Ln 101


# LANGUAGE_CODE = 'es-es'
LANGUAGE_CODE = 'es-co'

# TIME_ZONE = 'UTC'
TIME_ZONE =	'America/Bogota'

USE_I18N = True

USE_L10N = True

# USE_TZ = True
USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = 'staticfiles'

STATIC_PATH = os.path.join(PROJECT_PATH,'static')

MEDIA_ROOT = ''

MEDIA_URL = '/'

ADMIN_MEDIA_PREFIX = '/static/admin/'

TEMPLATE_DIRS = (
    'templates',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.request",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    
)

#AUTH_USER_MODEL = 'web.Usuario'
