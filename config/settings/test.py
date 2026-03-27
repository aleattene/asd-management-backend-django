"""
Test settings for ASD Management project.
"""

import os

# Must be set before importing base to satisfy the SECRET_KEY guard.
if not os.environ.get("SECRET_KEY"):
    os.environ["SECRET_KEY"] = "test-secret-key-long-enough-to-run-tests"

from .base import *  # noqa: F401, F403

DEBUG = False

# SQLite in-memory for fast tests
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Longer secret key to avoid JWT InsecureKeyLengthWarning
SECRET_KEY = "test-secret-key-that-is-long-enough-for-jwt-hmac-sha256"

# Faster password hashing for tests
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]
