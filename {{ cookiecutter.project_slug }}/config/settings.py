import secrets
from pathlib import Path

import environ

# --- setup and throat clearing
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
env.read_env(".env")

# --- basic setting
APP_NAME = env.str("FLY_APP_NAME", default="{{ cookiecutter.app_name }}")
DEBUG = env("DEBUG", cast=bool, default=False)
LANGUAGE_CODE = "en-us"
ROOT_URLCONF = "config.urls"
SECRET_KEY = env("SECRET_KEY", default=secrets.token_hex(32))
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
WSGI_APPLICATION = "config.wsgi.application"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# -- allowed_hosts and csrf origins
#    some malarky is necessary to support fly and tailscale
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])
for localhost in ("localhost", "127.0.0.1"):
    if localhost not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(localhost)
if "FLY_APP_NAME" in env:
    ALLOWED_HOSTS.append(f"{env('FLY_APP_NAME')}.fly.dev")
    CSRF_TRUSTED_ORIGINS = [f"https://{env('FLY_APP_NAME')}.fly.dev"]
if "TAILNET_DOMAIN" in env:
    # We can't use FLY_APP_NAME.tailnet because re-deploys end up with
    # different domain names (node-1, node-2, node-3, etc) from Tailscale.
    # But that's ok because the tailnet is always mine unlike fly.dev.
    ALLOWED_HOSTS.append(f".{env('TAILNET_DOMAIN')}")
    CSRF_TRUSTED_ORIGINS.append(f"https://*.{env('TAILNET_DOMAIN')}")

# --- static files, tailwind, etc
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / ".staticroot"
STATICFILES_DIRS = [BASE_DIR / "assets"]
TAILWIND_CLI_SRC_CSS = STATICFILES_DIRS[0] / "main.css"
TAILWIND_CLI_DIST_CSS = "dist/tailwind.css"

# --- apps, middleware, templates, databases
INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_browser_reload",
    "django_tailwind_cli",
    "whitenoise",
    "{{ cookiecutter.app_name }}",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

if "TAILNET_DOMAIN" in env:
    MIDDLEWARE.append("config.middleware.TailscaleAuthMiddleware")

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

DATABASES = {
    "default": env.db(default=f"sqlite:///{BASE_DIR}/db.sqlite3"),
}
