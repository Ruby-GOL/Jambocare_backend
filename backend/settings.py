from pathlib import Path
import os
from datetime import timedelta
import environ
import django_heroku

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
env = environ.Env()
environ.Env.read_env()


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-cb$usm+&s6us22g(5bhlkr9jx+t(e2mdrg8^$j0(o#v49%p_c3' #env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False #env('DEBUG') == 'True'

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt.token_blacklist',
    'django_filters',
    'django_rest_passwordreset',
    'drf_yasg',
    'drf_spectacular',
    # Media Cloudinary
    "cloudinary",
    "cloudinary_storage",

    'accounts',
    'chatbot',
    'translator',
    
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
  'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'Translator',
        'USER': 'fredricomosh',
        'PASSWORD': 'Ooy5SuRcn6UQ',
        'HOST': 'ep-crimson-poetry-07648100.us-east-2.aws.neon.tech',
        'PORT': '5432',
        'OPTIONS': {'sslmode': 'require'},
  }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'accounts.validators.LatinPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# STATIC_URL = '/static_django/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static_django/')


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
#        'rest_framework.authentication.SessionAuthentication',
#        'rest_framework.authentication.BasicAuthentication',
        'accounts.authenticate.CustomAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'EXCEPTION_HANDLER': 'backend.utils.custom_exception_handler',
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Chatbot API',
    'DESCRIPTION': 'API for Chatbot',
    'VERSION': '1.0.0',
    'SCHEMA_PATH_PREFIX': r'/api/v1',

}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=float(60)),# env('ACCESS_TOKEN_LIFETIME_MINUTES')
    'REFRESH_TOKEN_LIFETIME': timedelta(days=float(30)), #env('REFRESH_TOKEN_LIFETIME_DAYS')
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),

    # custom
    'AUTH_COOKIE': 'access',
    # Cookie name. Enables cookies if value is set.
    'AUTH_COOKIE_REFRESH': 'refresh',
    # A string like "example.com", or None for standard domain cookie.
    'AUTH_COOKIE_DOMAIN': None,
    # Whether the auth cookies should be secure (https:// only).
    'AUTH_COOKIE_SECURE': True,
    # Http only cookie flag.It's not fetch by javascript.
    'AUTH_COOKIE_HTTP_ONLY': True,
    'AUTH_COOKIE_PATH': '/',  # The path of the auth cookie.
    'AUTH_COOKIE_SAMESITE': 'Lax',
    # Whether to set the flag restricting cookie leaks on cross-site requests. This can be 'Lax', 'Strict', or None to disable the flag.
}

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://localhost:3000",
    "http://localhost:8080",
]

CORS_ALLOW_CREDENTIALS = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT=587
EMAIL_HOST_USER='adhingafredrick@gmai.com'
EMAIL_HOST_PASSWORD='Fred.9707.23'
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False

# EMAIL_HOST = env('EMAIL_HOST')
# EMAIL_USE_TLS = env('EMAIL_USE_TLS') == 'True'
# EMAIL_PORT = env('EMAIL_PORT')
# EMAIL_USE_SSL = env('EMAIL_USE_SSL') == 'True'
# EMAIL_HOST_USER = env('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

AUTH_USER_MODEL = "accounts.User"

# Media Files Settings

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dpesoiqvk', #env('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': '239277538961433', #env('CLOUDINARY_API_KEY'),
    'API_SECRET': 'Ak-dfKUiytDqeQx0J4XPjrJVUlo' #env('CLOUDINARY_API_SECRET'),
}

if DEBUG:
    MEDIA_URL = "/media/"
    MEDIA_ROOT = BASE_DIR / "media"
else:
    MEDIA_URL = "/media/"
    DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"


STATIC_URL = "/static/"
STATICFILES_DIRS = (BASE_DIR / "static",)
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# import dj_database_url

# db_from_env = dj_database_url.config(conn_max_age=500)
# DATABASES["default"].update(db_from_env)


# django_heroku.settings(locals())
# del DATABASES['default']['OPTIONS']['sslmode'] 

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}