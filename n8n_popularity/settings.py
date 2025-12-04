from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

# ===========================
# PATHS
# ===========================
BASE_DIR = Path(__file__).resolve().parent.parent

# ===========================
# LOAD ENV
# ===========================
load_dotenv()

TRIGGER_SECRET = os.getenv("TRIGGER_SECRET", "change_this_local_secret")

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("❌ DJANGO_SECRET_KEY is not set in environment variables.")

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# ===========================
# DEBUG & HOSTS
# ===========================
DEBUG = os.getenv("DEBUG", "False") == "True"

# Railway auto-assigns domain — allow all for now
ALLOWED_HOSTS = ["*", "localhost", "127.0.0.1"]

# ===========================
# APPS
# ===========================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    "rest_framework",
    "workflows",
]

# ===========================
# MIDDLEWARE
# ===========================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware", 
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = 'n8n_popularity.urls'

# ===========================
# TEMPLATES
# ===========================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'n8n_popularity.wsgi.application'

# ===========================
# DATABASE
# Railway: use SQLite OR PostgreSQL
# ===========================
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=False
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# For future PostgreSQL migration:
# if os.getenv("DATABASE_URL"):
#     import dj_database_url
#     DATABASES["default"] = dj_database_url.parse(
#         os.getenv("DATABASE_URL"),
#         conn_max_age=600,
#         ssl_require=False
#     )

# ===========================
# STATIC FILES
# ===========================
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "staticfiles"

# ===========================
# DEFAULT FIELD
# ===========================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
