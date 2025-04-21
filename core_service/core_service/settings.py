import os
from pathlib import Path
import urllib.parse

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', default='-asdf&*YJHKP908yuik')
DEBUG = os.getenv('DEBUG', default=True)

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
    'companies',
    'transactions',
    'financials',
    'inventory',
    'clothing',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core_service.middleware.AuthenticationMiddleware',
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

# Get the DATABASE_URL from environment
database_url = os.getenv('DATABASE_URL')

# Print database connection info for debugging
print(f"Database URL: {database_url}")

if database_url:
    # Parse the URL
    parsed_url = urllib.parse.urlparse(database_url)
    
    # Extract database connection details
    db_config = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': parsed_url.path[1:],  # Remove leading slash
        'USER': parsed_url.username,
        'PASSWORD': parsed_url.password,
        'HOST': parsed_url.hostname,
        'PORT': parsed_url.port or '5432',
    }
    
    print(f"Database config: {db_config}")
    
    DATABASES = {'default': db_config}
else:
    # Fallback configuration
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('POSTGRES_DB', 'core_db'),
            'USER': os.getenv('POSTGRES_USER', 'postgres'),
            'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'postgres'),
            'HOST': 'postgres',  # Docker service name
            'PORT': '5432',      # Default PostgreSQL port inside Docker
        }
    }
    
    print(f"Using fallback database config: {DATABASES['default']}")

# Authentication settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'core_service.auth.UserManagementJWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# User Management Service settings
USER_MANAGEMENT_SERVICE_URL = os.getenv('USER_MANAGEMENT_SERVICE_URL', 'http://user_management_service:8000')

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'