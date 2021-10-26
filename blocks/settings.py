"""
Django settings for blocks project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import logging
import sentry_sdk

from os import environ
from dotenv import load_dotenv

from pathlib import Path

from kombu import Queue, Exchange

from sentry_sdk.integrations.django import DjangoIntegration

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Environment Variable Setup
load_dotenv()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = environ["DJANGO_SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(environ["DJANGO_DEBUG"]))


# Sentry
if not DEBUG:
    sentry_sdk.init(
        dsn=environ["SENTRY_DSN"],
        integrations=[DjangoIntegration()],
        environment="production",
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0,
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True,
    )

    logging.info("Sentry SDK Activated")


# CORS
CORS_ORIGIN_ALLOW_ALL = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "data_store",
    "data_blocks",
    "computational_blocks",
    "signal_blocks",
    "strategy_blocks",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # django celery
    "django_celery_results",
    # django celery beat,
    "django_celery_beat",
    "rest_framework",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # 'django.middleware.csrf.CsrfViewMiddleware',
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "blocks.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "blocks.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": environ["DATABASE_NAME"],
        "USER": environ["DATABASE_USER"],
        "PASSWORD": environ["DATABASE_PASSWORD"],
        "HOST": environ["DATABASE_HOST"],
        "PORT": environ["DATABASE_PORT"],
    },
    "data_bank": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": environ["DATA_BANK_DATABASE_NAME"],
        "USER": environ["DATA_BANK_DATABASE_USER"],
        "PASSWORD": environ["DATA_BANK_DATABASE_PASSWORD"],
        "HOST": environ["DATA_BANK_DATABASE_HOST"],
        "PORT": environ["DATA_BANK_DATABASE_PORT"],
    },
}

DATABASE_ROUTERS = ["blocks.router.CheckerRouter"]


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Celery

CELERY_RESULT_BACKEND = f'db+postgresql://{environ["DATABASE_USER"]}:{environ["DATABASE_PASSWORD"]}@{environ["DATABASE_HOST"]}:{environ["DATABASE_PORT"]}/{environ["CELERY_BACKEND_DATABASE_NAME"]}'
CELERY_CACHE_BACKEND = "django-cache"
CELERY_BROKER_URL = environ["RABBIT_MQ_URL"]
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

CELERY_QUEUES = (Queue("data", Exchange("data"), routing_key="data_task"),)
