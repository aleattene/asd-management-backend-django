"""
Development settings for ASD Management project.
"""

import os

from .base import *  # noqa: F401, F403

DEBUG = True

# Raises KeyError if SECRET_KEY is not set — required even in development.
SECRET_KEY: str = os.environ["SECRET_KEY"]

# SQLite for local development
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# CORS — allow all in development
CORS_ALLOW_ALL_ORIGINS = True
