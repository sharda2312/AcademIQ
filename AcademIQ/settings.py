"""
Django settings for AcademIQ project with CSRF fixes for production.
"""

from pathlib import Path
import os

from whitenoise.storage import CompressedManifestStaticFilesStorage
from dotenv import load_dotenv
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-hoxh^^3k!va5-_j7gbvm5guu^ep9#1c9hdyao=ox#e_mvl5x#3")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "False") == "True"

AUTH_USER_MODEL = 'authapp.User'

# Updated ALLOWED_HOSTS with proper format
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# Static files settings
STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# CSRF settings for production
# Add your domain to the trusted origins
CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8000',
    'https://127.0.0.1:8000',
    "https://academiq-t5k5.onrender.com"
]

# If you know your Render URL, add it explicitly
if os.getenv("RENDER_EXTERNAL_URL"):
    CSRF_TRUSTED_ORIGINS.append(os.getenv("RENDER_EXTERNAL_URL"))
    
# Add any custom domain you've configured
if os.getenv("CUSTOM_DOMAIN"):
    protocol = "https://" if not os.getenv("CUSTOM_DOMAIN").startswith(("http://", "https://")) else ""
    CSRF_TRUSTED_ORIGINS.append(f"{protocol}{os.getenv('CUSTOM_DOMAIN')}")

# Security settings for production
if not DEBUG:
    # HTTPS settings
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_REFERRER_POLICY = "same-origin"

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Add WhiteNoise-specific settings
WHITENOISE_MANIFEST_STRICT = True
WHITENOISE_COMPRESS = True  # Enable compression
WHITENOISE_COMPRESS_TIMEOUT = 60  # Compression timeout in seconds

LOGIN_URL = '/login/'

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "landing",
    "quiz",
    "result",
    "authapp",
    "account",
    "AIquiz",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "AcademIQ.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = "AcademIQ.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'dj_db_conn_pool.backends.mysql',
        'NAME': os.getenv("MYSQL_ADDON_DB"),  
        'USER': os.getenv("MYSQL_ADDON_USER"),     
        'PASSWORD': os.getenv("MYSQL_ADDON_PASSWORD"),         
        'HOST': os.getenv("MYSQL_ADDON_HOST"),     
        'PORT': '3306',
        'POOL_OPTIONS': {  # Add connection pool options
            'POOL_SIZE': 20,  # Number of connections to keep open
            'MAX_OVERFLOW': 10,  # Max number of additional connections to open if needed
            'POOL_TIMEOUT': 30,  # Seconds to wait before timeout error when pool is full
            'POOL_RECYCLE': 1800,  # Seconds before a connection is recycled (30 minutes)
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Session Settings
SESSION_COOKIE_AGE = 86400  #  24 hours
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = False

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"