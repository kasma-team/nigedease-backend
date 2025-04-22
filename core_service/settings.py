import os
from pathlib import Path
import django_environ
import dj_database_url

env = django_environ.Env()
env.read_env()

# ... existing code ... 