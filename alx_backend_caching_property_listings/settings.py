from pathlib import Path
import os
import environ

env = environ.Env()
environ.Env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------------------------------------------------
# Core
# -------------------------------------------------------------------
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-insecure-change-me")
DEBUG = bool(int(os.getenv("DJANGO_DEBUG", "1")))
ALLOWED_HOSTS = [h.strip() for h in os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",") if h.strip()]

# -------------------------------------------------------------------
# Applications
# -------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Local apps
    "properties",

    # NOTE: Do NOT add "django_redis" here. It's a cache backend, not an app.
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Optional: whole-site cache can be added later using:
    # "django.middleware.cache.UpdateCacheMiddleware",
    # ... (other middleware)
    # "django.middleware.cache.FetchFromCacheMiddleware",
]

ROOT_URLCONF = "alx-backend-caching_property_listings.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "alx-backend-caching_property_listings.wsgi.application"

# -------------------------------------------------------------------
# Database: PostgreSQL via Docker
# -------------------------------------------------------------------
POSTGRES_DB = os.getenv("POSTGRES_DB", "propertydb")
POSTGRES_USER = os.getenv("POSTGRES_USER", "propertyuser")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "propertypass")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")  # if running Django outside Docker
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "propertydb"),
        "USER": os.getenv("POSTGRES_USER", "propertyuser"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "propertypass"),
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}

# -------------------------------------------------------------------
# Cache: Redis via django-redis
# -------------------------------------------------------------------
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")  # service name "redis" if Django runs in Docker
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "1"))

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # pool settings help under load
            "CONNECTION_POOL_KWARGS": {"max_connections": 100, "encoding": "utf-8"},
            # "PASSWORD": os.getenv("REDIS_PASSWORD"),  # if you secure Redis
        },
        "KEY_PREFIX": "prop",
        "TIMEOUT": 60 * 5,  # default item TTL: 5 minutes
    }
}

# Use cache for sessions (faster than DB sessions)
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# (If you later enable whole-site caching middleware)
CACHE_MIDDLEWARE_SECONDS = 60
CACHE_MIDDLEWARE_KEY_PREFIX = "site"

# -------------------------------------------------------------------
# Internationalization & Time
# -------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Addis_Ababa"
USE_I18N = True
USE_TZ = True

# -------------------------------------------------------------------
# Static files
# -------------------------------------------------------------------
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# -------------------------------------------------------------------
# Logging: surface cache & DB behavior for performance analysis
# -------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {"format": "[{levelname}] {name}: {message}", "style": "{"},
        "verbose": {
            "format": "[{levelname}] {asctime} {name} {module}:{lineno} — {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "simple"},
    },
    "loggers": {
        "django.db.backends": {
            "handlers": ["console"],
            "level": "INFO" if DEBUG else "WARNING",
        },
        "django_redis": {
            "handlers": ["console"],
            "level": "DEBUG",  # shows cache hits/misses & redis ops
        },
    },
}
