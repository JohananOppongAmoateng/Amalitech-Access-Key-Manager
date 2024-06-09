"""
Django settings for AccessKeyManager project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from pathlib import Path
from dotenv import load_dotenv
# Import dj-database-url at the beginning of the file.
import dj_database_url

load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY","django-insecure-9z+4ci&iqo+l4jnh99zytt5y09bgb$p%e__$hy1a^4ts)iuafn")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG =  True

ALLOWED_HOSTS = ['localhost:8000',"amalitech-access-key-manager.onrender.com"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "registration",
    "accesskey",

    'drf_spectacular',
    'rest_framework',
    'crispy_forms',
    "crispy_bootstrap5",
]
SITE_ID = 1

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "AccessKeyManager.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "AccessKeyManager.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    # "default": {
    #     "ENGINE": "django.db.backends.sqlite3",
    #     "NAME": BASE_DIR / "prod.sqlite3",
    # }
    # 
    'default': dj_database_url.config(default="postgres://johanan:wnE9F8l27fLfbaiVA2uNE7LlqSjXlCxs@dpg-cpie6tmct0pc73fql94g-a.oregon-postgres.render.com/akm",conn_max_age=600)
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "registration.CustomUser"

LOGIN_REDIRECT_URL = '/'
SIGNUP_REDIRECT_URL = '/accounts/login'
LOGOUT_REDIRECT_URL = '/accounts/login'

ACCOUNT_ACTIVATION_DAYS = 7

EMAIL_HOST = "smtp"
EMAIL_PORT = 587


IMPORT_EXPORT_USE_TRANSACTIONS = True

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"


# Registration App account settings
ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_EMAIL_SUBJECT_PREFIX = "[Access Key Manager] "
SEND_ACTIVATION_EMAIL = True




# Using the new No Captcha reCaptcha
NOCAPTCHA = True

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = False
ACCOUNT_EMAIL_VERIFICATION = ("mandatory",)
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300
ACCOUNT_USERNAME_MIN_LENGTH = 3


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

CRONJOBS = [
    ('0 0 * * *', 'accesskey.management.commands.update_expired_keys'),
    
]
DEFAULT_FROM_EMAIL = "johananoppongamoateng2001@gmail.com"


REST_FRAMEWORK = {
    # YOUR SETTINGS
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Access Key Manager API',
    'DESCRIPTION': 'API for Access Key Manager',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}