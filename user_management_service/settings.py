import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Comment out the AUTH_USER_MODEL setting since we're using MongoDB
# AUTH_USER_MODEL = 'users.User'

# Django still needs a database configuration even though we're using MongoDB
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
} 