# ----------------------------------------------------------------------------------+
#                                                                                   |
#                                      IMPORTS                                      |
#                                                                                   |
# ----------------------------------------------------------------------------------+

import datetime
from pathlib import Path

# ----------------------------------------------------------------------------------+
#                                                                                   |
#                                     MERCHANT                                      |
#                                                                                   |
# ----------------------------------------------------------------------------------+


MERCHANT = '960f109b-2404-4f2e-9c58-7f250a54f74f'


# ----------------------------------------------------------------------------------+
#                                                                                   |
#                                      SECURITY                                     |
#                                                                                   |
# ----------------------------------------------------------------------------------+


BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-d=v=t!s=yyho4i(r597@*28rs0m^ddjangodcsz(kjx&*@*5)s)=vv3"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

WHOAMI = "http://127.0.0.1:8000/" if DEBUG else "https://currencyno-server.iran.liara.com/"
FRONT = "http://127.0.0.1:3000/store" if DEBUG else "https://currencyno.iran.liara.com/"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 6,
        }
    },
    {
        "NAME": "Auth.validators.PinValidator"
    },
]

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": datetime.timedelta(days=365),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,

}


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    )
}


# ----------------------------------------------------------------------------------+
#                                                                                   |
#                                        CORS                                       |
#                                                                                   |
# ----------------------------------------------------------------------------------+


ALLOWED_HOSTS = ["*"]


# cors
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://currencyno.com",
    "http://currencyno.com",
]


# ----------------------------------------------------------------------------------+
#                                                                                   |
#                                   INSTALLED APPS                                  |
#                                                                                   |
# ----------------------------------------------------------------------------------+


DEPENDENCIES = [
    "rest_framework",
    "corsheaders",
    'requests'
]

MAIN_APPS = [
    "Apps.Orders.apps.OrdersConfig",
    "Apps.User.apps.UserConfig",
    "Apps.Products.apps.ProductsConfig",
    "Apps.Core.apps.CoreConfig",

    "Apps.Fix.apps.FixConfig",
    "Apps.Academy.apps.AcademyConfig",
    "Apps.Work.apps.WorkConfig",
    "Apps.Caffeh.apps.CaffehConfig",

    "Auth",
    "Finance"
]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    *DEPENDENCIES,
    *MAIN_APPS,
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ----------------------------------------------------------------------------------+
#                                                                                   |
#                                     DEFINITION                                    |
#                                                                                   |
# ----------------------------------------------------------------------------------+


ROOT_URLCONF = "SERVER.urls"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "SERVER.wsgi.application"


# ----------------------------------------------------------------------------------+
#                                                                                   |
#                                  DATABASE & FILES                                 |
#                                                                                   |
# ----------------------------------------------------------------------------------+


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "data/db.sqlite3",
    }
}

STATIC_URL = "static/"
AUTH_USER_MODEL = "User.BaseUser"


# ----------------------------------------------------------------------------------+
#                                                                                   |
#                               INTERNATIONALIZATION                                |
#                                                                                   |
# ----------------------------------------------------------------------------------+


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True
