"""
Django settings for MeterLab project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# my static dir
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMP_DIR = os.path.join(BASE_DIR, "templates")


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'cniyhb@tr-#mw)5)ta_ln*1g&0u4r9o&ryl+b=uo)apb(^@!)5'
ENCRYPT_KEY = 'cniyhb@tr-#mw)5)ta_ln*1g&0u4r9o&ryl+b=uo)apb(^@!)5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['192.168.1.4', 'localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sweetify',
    'Acquisitions',
    'Meters',
    'Signatory',
    'Calibration',
    'Users',
    'Assign',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.contrib.sessions.serializers.PickleSerializer'
]

ROOT_URLCONF = 'MeterLab.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates/"],
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

WSGI_APPLICATION = 'MeterLab.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'zanecometerpy',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': 'blaise',
        'PORT': '3306',
        'CONN_MAX_AGE': 290,
    },
    'warehouse': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'zanecoinvphp',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': 'blaise',
        'PORT': '3306',
        'CONN_MAX_AGE': 290,
    },
    'OPTIONS': {
        'connect_timeout': 5,
    }
}
DATABASE_ROUTERS = ['MeterLab.routers.AppRouter']


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    STATIC_DIR,
]

LOGIN_REDIRECT_URL = '/'

AREA_CHOICES = (
    ('0', 'Dipolog Main Office'),
    ('1', 'Piñan Area Services'),
    ('2', 'Sindangan Area Services'),
    ('3', 'Liloy Area Services'),
)

SWEETIFY_SWEETALERT_LIBRARY = 'sweetalert2'

# Logout after a period of inactivity
# INACTIVE_TIME = 3*60  # 3 minutes - or whatever period you think appropriate
# SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# SESSION_COOKIE_AGE = INACTIVE_TIME   # change expired session
# SESSION_IDLE_TIMEOUT = INACTIVE_TIME  # logout

# Auto logout delay in minutes
# AUTO_LOGOUT_DELAY = 5  # equivalent to 5 minutes
