"""
Django settings for DjangoPostingSite project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv() # load env vars

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-nie)(!0_j46oo9)bvq-ke0+!@u)!#=5c!pr^hc(jz-w)k%2f6="

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOWED_ORIGINS = ['https://f774-120-229-48-157.ngrok-free.app']
CSRF_TRUSTED_ORIGINS = ['https://f774-120-229-48-157.ngrok-free.app']
# Application definition

INSTALLED_APPS = [
    "guardian", # per object permission

    "daphne", # django channels

    "corsheaders", # cors headers

    "simpleui",  # admin simple ui

    "posts.apps.PostsConfig",  # posts app

    "rest_framework",  # django rest framework

    "django_social_share", # django social share

    "taggit",  # taggit for tagging support
    "taggit_templatetags2",

    "my_comments.apps.MyCommentsConfig",
    "fluent_comments", # comments and crispy forms
    "crispy_bootstrap4",
    "crispy_forms",
    "django_comments",


    "allauth_ui", # allauth ui and authentication
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.github",  # for login with github account
    "allauth.socialaccount.providers.google",  # for login with google account
    "widget_tweaks",  # must after allauth

    "martor", # markdown editor

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
]

MIDDLEWARE = [


    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",

]

ROOT_URLCONF = "DjangoPostingSite.urls"

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

                "django.template.context_processors.request",

                "posts.context_processors.site_settings",
                "posts.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "DjangoPostingSite.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    "django.contrib.auth.context_processors.PermWrapper"
)

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = "static/"
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder", # for finding static files in app folders
]
MEDIA_ROOT = BASE_DIR / 'uploads' # the name of the media folder
MEDIA_URL = "/media/" # the base url for media files
DEFAULT_IMAGE_FOLDER = MEDIA_ROOT / "default"
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Markdown Editor Settings
MARTOR_THEME = "bootstrap"
MARTOR_ENABLE_CONFIGS = {
    'imgur': 'true',     # to enable/disable imgur uploader/custom uploader.
    'mention': 'true',   # to enable/disable mention
    'jquery': 'true',    # to include/revoke jquery (require for admin default django)
}
MARTOR_UPLOAD_PATH = MEDIA_ROOT / 'martor'
MARTOR_UPLOAD_URL = '/api/uploader/'  # change to local uploader
MAX_IMAGE_UPLOAD_SIZE =  104857600

# allauth settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",

    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",

    # # hook django-guardian backend
    "guardian.backends.ObjectPermissionBackend",
]
SITE_ID = 1
ACCOUNT_PREVENT_ENUMERATION= False # setting this to false prevents violating the email unique constraints when login with social account!!!
SOCIALACCOUNT_ADAPTER = "DjangoPostingSite.account.adapters.MySocialAccountAdapter" # auto-connect social account with existing local accounts
ACCOUNT_AUTHENTICATION_METHOD="username_email" # user either username or email to authenticate
ACCOUNT_EMAIL_REQUIRED = True # Must have email
ACCOUNT_EMAIL_VERIFICATION='mandatory' # Must verify email

ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
ACCOUNT_SESSION_REMEMBER = True

ACCOUNT_UNIQUE_EMAIL = True
LOGIN_REDIRECT_URL = "posts:index" # uses namespace instead of actual url!
ACCOUNT_LOGOUT_REDIRECT_URL = "posts:index"

# Email settings (must have this if using smtp backend)
import json
EMAIL_USE_TLS = True
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_PORT = os.environ.get("EMAIL_PORT")
# print(f"EMAIL_HOST:{EMAIL_HOST} EMAIL_HOST_USER:{EMAIL_HOST_USER} EMAIL_HOST_PASSWORD:{EMAIL_HOST_PASSWORD}")

SOCIALACCOUNT_PROVIDERS = {
    'google':{ # allauth google settings
        'SCOPE':[
            'profile',
            'email',
        ],
        'AUTH_PARAMS':{
            'access_type':'offline',
        },
        'OAUTH_PKCE_ENABLED': True,
    } # github doesn't require settings
}

# fluent comments settings
CRISPY_TEMPLATE_PACK = 'bootstrap4'
COMMENTS_APP='fluent_comments'
FLUENT_COMMENTS_FORM_CLASS = 'my_comments.forms.ModifiedCommentForm'
# FLUENT_COMMENTS_EXCLUDE_FIELDS = ('preview',)
# drf settings
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}

# django whitenoise settings
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# django channels settings
ASGI_APPLICATION = "DjangoPostingSite.asgi.application" # custom asgi app
