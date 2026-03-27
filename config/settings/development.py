"""
Development settings for ASD Management project.
"""

from .base import *  # noqa: F401, F403

DEBUG = True

# SQLite for local development
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# CORS — allow all in development
CORS_ALLOW_ALL_ORIGINS = True
