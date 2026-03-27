"""
Production settings for ASD Management project.
"""

import os

import environ

from .base import *  # noqa: F401, F403

DEBUG = False

# Raises ImproperlyConfigured if SECRET_KEY is not set in the environment
SECRET_KEY: str = environ.Env()("SECRET_KEY")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DATABASE"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}

# Security
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
# Reverse proxy support (nginx/caddy terminate TLS and forward plain HTTP internally).
# WARNING: if the app is reachable without a proxy, X-Forwarded-Proto can be spoofed.
# SECURE_SSL_REDIRECT defaults to true only when TRUST_PROXY_SSL_HEADER is also true,
# preventing an infinite redirect loop in proxy deployments where Django sees plain HTTP.
TRUST_PROXY_SSL_HEADER: bool = os.getenv("TRUST_PROXY_SSL_HEADER", "false").lower() in ("true", "1", "yes")
_ssl_redirect_default: str = "true" if TRUST_PROXY_SSL_HEADER else "false"
SECURE_SSL_REDIRECT: bool = os.getenv("SECURE_SSL_REDIRECT", _ssl_redirect_default).lower() in ("true", "1", "yes")
if TRUST_PROXY_SSL_HEADER:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# HSTS — env-driven to allow safe staging/first deploys.
# Enable preload only after confirming the entire domain surface is HTTPS-ready.
# WARNING: SECURE_HSTS_PRELOAD=true submits the domain to browser preload lists — hard to reverse.
SECURE_HSTS_SECONDS: int = environ.Env().int("SECURE_HSTS_SECONDS", default=31536000)
SECURE_HSTS_INCLUDE_SUBDOMAINS: bool = os.getenv("SECURE_HSTS_INCLUDE_SUBDOMAINS", "false").lower() in ("true", "1", "yes")
SECURE_HSTS_PRELOAD: bool = os.getenv("SECURE_HSTS_PRELOAD", "false").lower() in ("true", "1", "yes")
