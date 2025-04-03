import os
from pathlib import Path
from environ import Env

env = Env()
Env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env.str('SECRET_KEY', default='-asdf&*YJHKP908yuik')
DEBUG = env.bool('DEBUG', default=True) # type: ignore

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_yasg',
    'financial.apps.FinancialConfig',
    'product.apps.ProductConfig',
    'inventory.apps.InventoryConfig',
    'djongo',  # Add Djongo here
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core_service.urls'

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
        },
    },
]

WSGI_APPLICATION = 'core_service.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': env.str('DB_NAME', 'core_service_db'),  # MongoDB database name
        'CLIENT': {
            'host': env.str('DB_HOST', 'localhost'),
            'port': env.int('DB_PORT', 27017),  # Default MongoDB port # type: ignore
        }
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'