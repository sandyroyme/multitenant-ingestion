import os
import environ
from pathlib import Path
env = environ.Env()
environ.Env.read_env()
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = env('DJANGO_SECRET_KEY', default='unsafe-secret-key')
DEBUG = True
ALLOWED_HOSTS = []
INSTALLED_APPS = [
    'django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes',
    'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles',
    'rest_framework', 'ingestion',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware', 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware', 'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'multitenant_ingestion.urls'
TEMPLATES = [{'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'ingestion' / 'templates'], 'APP_DIRS': True,
    'OPTIONS': {'context_processors': [
        'django.template.context_processors.debug', 'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth', 'django.contrib.messages.context_processors.messages',
    ]},
}]
WSGI_APPLICATION = 'multitenant_ingestion.wsgi.application'
DATABASES = {'default': env.db(default='sqlite:///db.sqlite3')}
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
# AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
KAFKA_BROKER_URL = env('KAFKA_BROKER_URL')
KAFKA_TOPIC = env('KAFKA_TOPIC', default='file_uploaded')
KAFKA_FAILURE_TOPIC = env('KAFKA_FAILURE_TOPIC', default='file_failed')
