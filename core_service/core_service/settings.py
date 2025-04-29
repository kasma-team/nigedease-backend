import os
from pathlib import Path
<<<<<<< Updated upstream
=======
import urllib.parse
from datetime import timedelta
>>>>>>> Stashed changes

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

<<<<<<< Updated upstream
SECRET_KEY = os.getenv('SECRET_KEY', default='-asdf&*YJHKP908yuik')
DEBUG = os.getenv('DEBUG', default=True)
=======
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-a2_f2@06^39@o#r6+$w=+*!6o+u_k3ckuer@&di)vu(gfm4p9u')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'nigedease-secret-key-2024')
DEBUG = True
>>>>>>> Stashed changes

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
<<<<<<< Updated upstream
=======
    'rest_framework_simplejwt',
    'drf_yasg',
    'corsheaders',  # Add CORS headers
>>>>>>> Stashed changes
    'companies',
    'transactions',
    'financials',
    'inventory',
    'clothings',
    'drf_spectacular',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Add CORS middleware
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

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
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'core_service'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'), 
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

REST_FRAMEWORK = {
<<<<<<< Updated upstream
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
     'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # 👈 use JWTAuthentication here!
    ],
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Core Service API',
    'DESCRIPTION': 'API documentation for Core Service',
    'VERSION': 'v1',
    'SERVE_INCLUDE_SCHEMA': True,
    'CONTACT': {'email': 'contact@example.com'},
    'LICENSE': {'name': 'BSD License'},
    'TOS': 'https://www.google.com/policies/terms/',
}

=======
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'core_service.auth.UserManagementJWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=int(os.getenv('JWT_ACCESS_TOKEN_LIFETIME', 5))),
    'REFRESH_TOKEN_LIFETIME': timedelta(minutes=int(os.getenv('JWT_REFRESH_TOKEN_LIFETIME', 1440))),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'SIGNING_KEY': os.getenv('JWT_SECRET_KEY', SECRET_KEY),  # Use environment variable with fallback
}

# Swagger settings
SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'DEFAULT_INFO': 'core_service.urls.schema_view',
}

# User Management Service settings
USER_MANAGEMENT_SERVICE_URL = os.getenv('USER_MANAGEMENT_SERVICE_URL', 'http://user_management_service:8000')
>>>>>>> Stashed changes

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
        'core_service': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}